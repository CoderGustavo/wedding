from starlette.exceptions import HTTPException
from bson import ObjectId
from pymongo import MongoClient, errors as pymongo_errors
import boto3
from botocore.config import Config
from os import getenv
import re
from datetime import datetime, timedelta

from time import time

from utilities.Reusable import Reusable
from utilities.Logger import logger

from dotenv import load_dotenv

# Load environment variables from a .env file for security
load_dotenv()

class BaseClass:
    def __init__(self):
        # Initialize class variables
        self.defaultFilter = {}
        self.db_name = getenv("MONGO_DB_NAME", "default_db")
        self.collection_name = None  # Set this in child classes

        # Initialize MongoDB client
        self.mongo_client = MongoClient(getenv("MONGO_URI", "mongodb://localhost:27017"), serverSelectionTimeoutMS=5000)
        self.db = self.mongo_client[self.db_name]

        # Initialize Cloudflare R2 client
        try:
            config = Config(
                connect_timeout=5,
                read_timeout=5
            )
            self.s3_client = boto3.client(
                's3',
                endpoint_url=getenv("R2_ENDPOINT_URL", "https://test.com"),
                aws_access_key_id=getenv("R2_ACCESS_KEY_ID", "123"),
                aws_secret_access_key=getenv("R2_SECRET_ACCESS_KEY", "1234"),
                config=config
            )
        except Exception:
            logger.error("Failed to initialize S3 client")
            print(getenv("R2_ENDPOINT_URL"))
            print(getenv("R2_ACCESS_KEY_ID"))
            self.s3_client = None
        self.bucket_name = getenv("R2_BUCKET_NAME", "default")

    def _safe_db_operation(self, operation, *args, **kwargs):
        """
        Helper method to safely perform a MongoDB operation with a timeout of 5 seconds.
        """
        try:
            start_time = time()
            result = operation(*args, **kwargs)
            end_time = time()
            if end_time - start_time > 5:
                raise HTTPException(status_code=504, detail="Database operation timeout")
            return result
        except pymongo_errors.ServerSelectionTimeoutError:
            raise HTTPException(status_code=504, detail="Database operation timeout error")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database operation failed: {str(e)}")

    def sanitize_input(self, value):
        """Sanitize input to prevent issues (MongoDB does not require heavy sanitization)."""
        return Reusable().sanitize_input(value)

    def create_one(self, item: dict):

        try:
            # Insert the document into the collection
            result = self.db[self.collection_name].insert_one(item)
            new_item = self.db[self.collection_name].find_one({"_id": result.inserted_id})
        except Exception as e:
            logger.error(f"Error creating document in {self.collection_name}: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Error creating document")

        return {self.collection_name: [Reusable().convert_objectid_to_str(new_item)]}

    def delete_one(self, id: str):
        try:
            # Update the document to mark it as deleted
            result = self.db[self.collection_name].update_one(
                {"_id": ObjectId(id)},
                {"$set": {"deleted": True}}
            )
            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Document not found")
        except Exception as e:
            logger.error(f"Error deleting document: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Error deleting document")

        return {"success": True, "msg": f"{self.collection_name} deleted successfully!"}

    def get_all(self):
        try:
            # Query all documents with default filter
            documents = list(self.db[self.collection_name].find(self.defaultFilter))
        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            raise HTTPException(status_code=400, detail="Error retrieving documents")

        return {self.collection_name: Reusable().convert_objectid_to_str(documents)}

    def get_all_by_filter(self, filter: dict, collection_name: str = None):
        self.collection_name = collection_name if collection_name else self.collection_name
        try:
            sanitized_filter = {k: self.sanitize_input(v) for k, v in filter.items()}
            filter_query = {**self.defaultFilter, **sanitized_filter}
            documents = list(self.db[self.collection_name].find(filter_query))
        except Exception as e:
            logger.error(f"Error retrieving filtered documents: {str(e)}")
            raise HTTPException(status_code=400, detail="Error retrieving filtered documents")

        return {self.collection_name: Reusable().convert_objectid_to_str(documents)}

    def get_one_by_id(self, id: str):
        try:
            doc = self.db[self.collection_name].find_one({"_id": ObjectId(id), **self.defaultFilter})
            if not doc:
                raise HTTPException(status_code=404, detail="Document not found")
        except Exception as e:
            logger.error(f"Error retrieving document: {str(e)}")
            raise HTTPException(status_code=400, detail="Error retrieving document")

        return {self.collection_name: [Reusable().convert_objectid_to_str(doc)]}

    def update_one(self, id: str, item: dict, files: dict):
        try:
            result = self.db[self.collection_name].update_one(
                {"_id": ObjectId(id)},
                {"$set": item}
            )
            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Document not found")
            updated_item = self.db[self.collection_name].find_one({"_id": ObjectId(id)})
        except Exception as e:
            logger.error(f"Error updating document: {str(e)}")
            raise HTTPException(status_code=400, detail="Error updating document")

        return {self.collection_name: [Reusable().convert_objectid_to_str(updated_item)]}

    def _upload_image(self, file):
        """Upload image file to Cloudflare R2 and return the public URL."""
        try:
            # Unique name for the image
            timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
            file_key = f"{self.collection_name}/{timestamp}_{Reusable().random_number()}.webp"

            # Upload the file to R2
            self.s3_client.upload_fileobj(
                file.file,
                self.bucket_name,
                file_key,
                ExtraArgs={'ContentType': file.content_type, 'ACL': 'public-read'}
            )

            # Return the public URL from Cloudflare R2
            return f"{getenv('R2_CDN_URL')}/{file_key}"

        except Exception as e:
            raise HTTPException(status_code=500, detail="Image upload failed")


    def validate_confirmation_period(self, confirmation_data: dict) -> None:
        confirmation_periods = [
            {
                "start_date": datetime(2024, 1, 1),
                "end_date": datetime(2024, 7, 31)
            },
            {
                "start_date": datetime(2024, 8, 1),
                "end_date": datetime(2024, 12, 31)
            },
            {
                "start_date": datetime(2025, 1, 1),
                "end_date": datetime(2025, 4, 30)
            }
        ]

        try:
            existing_confirmations = self._safe_db_operation(
                self.get_all_by_filter,
                {
                    "guest_id": confirmation_data.get("guest_id"),
                },
                "confirmations"
            )

            if existing_confirmations.get("confirmations", {}):
                actual_period = {}

                confirmation_date = confirmation_data.get("created_at")
                for period in confirmation_periods:
                    if isinstance(confirmation_date, str):
                        confirmation_date = datetime.strptime(confirmation_date, "%Y-%m-%dT%H:%M:%S.%f")
                    elif not isinstance(confirmation_date, datetime):
                        confirmation_date = datetime.now()

                    if period["start_date"] <= confirmation_date <= period["end_date"]:
                        actual_period = period
                        break

                invalid_date = datetime.now() - timedelta(days=730)

                for confirmation in existing_confirmations["confirmations"]:
                    confirmation_date = confirmation.get("created_at")

                    if isinstance(confirmation_date, str):
                        confirmation_date = datetime.strptime(confirmation_date, "%Y-%m-%dT%H:%M:%S.%f")
                    elif not isinstance(confirmation_date, datetime):
                        confirmation_date = invalid_date

                    if actual_period["start_date"] <= confirmation_date <= actual_period["end_date"]:

                        raise HTTPException(
                            status_code=400,
                            detail="Já existe uma confirmação para este convidado neste período"
                        )
        except Exception as e:
            if not isinstance(e, HTTPException):
                raise HTTPException(
                    status_code=500,
                    detail=f"Erro ao verificar confirmações existentes: {str(e)}"
                )
            raise e
        return True
