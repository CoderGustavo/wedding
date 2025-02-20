from bson import ObjectId
from .base import BaseClass
from utilities.Reusable import Reusable
from fastapi import HTTPException
from dotenv import load_dotenv
from typing import Optional
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

class GuestController(BaseClass):
    def __init__(self):
        """
        Initializes the GuestController by defining the specific MongoDB collection.
        """
        super().__init__()
        self.collection_name = "guests"  # MongoDB collection name for wedding guests

    def create_guest(self, guest_data: dict) -> dict:
        """
        Adds a new guest to the MongoDB collection.
        """

        return self._safe_db_operation(self.create_one, guest_data)

    def get_guests(self) -> dict:
        """
        Retrieves all registered guests.
        """
        return self._safe_db_operation(self.get_all)

    def get_guests_by_phone(self, phone: str) -> Optional[dict]:
        """
        Retrieves a guest by ID.
        """
        try:
            result = self._safe_db_operation(self.get_all_by_filter, {"phone": phone})
            result_fixed = Reusable().convert_objectid_to_str(result) if result else None
            if result_fixed.get("guests"):
                for guest in result_fixed.get("guests"):
                    guest["confirmed"] = True
                    try:
                        has_confirmed = self.validate_confirmation_period({
                            "guest_id": guest.get("id"),
                            "created_at": datetime.now()
                        })
                        print(has_confirmed)
                        if has_confirmed:
                            guest["confirmed"] = False
                    except Exception as e:
                        guest["confirmed"] = True
            return result_fixed
        except Exception as e:
            import traceback
            print(''.join(traceback.format_tb(e.__traceback__)))
            raise HTTPException(status_code=500, detail=f"Error retrieving guest by Phone: {str(e)}")

    def get_guest_by_id(self, guest_id: str) -> Optional[dict]:
        """
        Retrieves a guest by ID.
        """
        try:
            result = self._safe_db_operation(self.get_one_by_id, ObjectId(guest_id))
            return Reusable().convert_objectid_to_str(result) if result else None
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving guest by ID: {str(e)}")

    def update_guest(self, guest_id: str, guest_data: dict, files: Optional[dict] = None) -> dict:
        """
        Updates a guest's data by ID.
        """
        try:
            result = self._safe_db_operation(self.update_one, ObjectId(guest_id), guest_data, files)  # Converts ID
            return Reusable().convert_objectid_to_str(result) if result else None
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating guest: {str(e)}")

    def delete_guest(self, guest_id: str) -> dict:
        """
        Soft deletes a guest by ID.
        """
        try:
            result = self._safe_db_operation(self.delete_one, ObjectId(guest_id))  # Converts string to ObjectId
            return {"success": True, "msg": "Guest successfully deleted"} if result else None
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting guest: {str(e)}")
