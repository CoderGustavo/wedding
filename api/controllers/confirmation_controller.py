from bson import ObjectId
from .base import BaseClass
from utilities.Reusable import Reusable
from fastapi import HTTPException
from dotenv import load_dotenv
from typing import Optional
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

class ConfirmationController(BaseClass):
    def __init__(self):
        """
        Initializes the ConfirmationController by defining the specific MongoDB collection.
        """
        super().__init__()
        self.collection_name = "confirmations"  # MongoDB collection name for confirmations

    def create_confirmation(self, confirmation_data: dict) -> dict:
        """
        Adds a new confirmation to the MongoDB collection.
        """

        self.validate_confirmation_period(confirmation_data)
        return self._safe_db_operation(self.create_one, confirmation_data)

    def get_confirmations(self) -> dict:
        """
        Retrieves all confirmation records.
        """
        return self._safe_db_operation(self.get_all)

    def get_confirmations_by_guest_id(self, guest_id: str) -> Optional[dict]:
        """
        Retrieves confirmations by associated guest id.
        """
        try:
            result = self._safe_db_operation(self.get_all_by_filter, {"guest_id": guest_id})
            return Reusable().convert_objectid_to_str(result) if result else None
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving confirmations by guest_id: {str(e)}")

    def get_confirmation_by_id(self, confirmation_id: str) -> Optional[dict]:
        """
        Retrieves a confirmation by ID.
        """
        try:
            result = self._safe_db_operation(self.get_one_by_id, ObjectId(confirmation_id))
            return Reusable().convert_objectid_to_str(result) if result else None
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving confirmation by ID: {str(e)}")

    def update_confirmation(self, confirmation_id: str, confirmation_data: dict) -> dict:
        """
        Updates a confirmation's data by ID.
        """
        try:
            result = self._safe_db_operation(self.update_one, ObjectId(confirmation_id), confirmation_data)
            return Reusable().convert_objectid_to_str(result) if result else None
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating confirmation: {str(e)}")

    def delete_confirmation(self, confirmation_id: str) -> dict:
        """
        Soft deletes a confirmation by ID.
        """
        try:
            result = self._safe_db_operation(self.delete_one, ObjectId(confirmation_id))
            return {"success": True, "msg": "Confirmation successfully deleted"} if result else None
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting confirmation: {str(e)}")