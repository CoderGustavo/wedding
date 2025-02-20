from bson import ObjectId
from .base import BaseClass
from utilities.Reusable import Reusable
from fastapi import HTTPException
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()

class GiftController(BaseClass):
    def __init__(self):
        """
        Initializes the GiftController by defining the specific MongoDB collection.
        """
        super().__init__()
        self.collection_name = "gifts"  # MongoDB collection name for gifts

    def create_gift(self, gift_data: dict, photo: Optional[dict] = None) -> dict:
        """
        Adds a new gift to the MongoDB collection.
        """

        if not photo:
            raise HTTPException(status_code=402, detail=f"One image must be sent.")

        gift_data["payment_url"] = str(gift_data["payment_url"])
        uploaded_image_url = self._upload_image(photo)
        gift_data["image"] = uploaded_image_url

        return self._safe_db_operation(self.create_one, gift_data)

    def get_gifts(self) -> dict:
        """
        Retrieves all registered gifts.
        """
        return self._safe_db_operation(self.get_all)

    def get_gift_by_id(self, gift_id: str) -> Optional[dict]:
        """
        Retrieves a gift by ID.
        """
        try:
            result = self._safe_db_operation(self.get_one_by_id, ObjectId(gift_id))  # Converts string to ObjectId
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving gift by ID: {str(e)}")

    def update_gift(self, gift_id: str, gift_data: dict, files: Optional[dict] = None) -> dict:
        """
        Updates a gift's data by ID.
        """
        try:
            result = self._safe_db_operation(self.update_one, ObjectId(gift_id), gift_data, files)  # Converts ID
            return Reusable().convert_objectid_to_str(result) if result else None
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating gift: {str(e)}")

    def delete_gift(self, gift_id: str) -> dict:
        """
        Soft deletes a gift by ID.
        """
        try:
            result = self._safe_db_operation(self.delete_one, ObjectId(gift_id))  # Converts string to ObjectId
            return {"success": True, "msg": "Gift successfully deleted"} if result else None
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting gift: {str(e)}")
