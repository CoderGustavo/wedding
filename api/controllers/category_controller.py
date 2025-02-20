from bson import ObjectId
from .base import BaseClass
from utilities.Reusable import Reusable
from fastapi import HTTPException, UploadFile
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()

class CategoryController(BaseClass):
    def __init__(self):
        """
        Initializes the CategoryController by defining the specific MongoDB collection.
        """
        super().__init__()
        self.collection_name = "categories"  # MongoDB collection name for categories

    def create_category(self, category_data: dict, image: Optional[UploadFile] = None) -> dict:
        """
        Adds a new category to the MongoDB collection.
        """

        uploaded_image_url = self._upload_image(image)
        category_data["image"] = uploaded_image_url

        return self._safe_db_operation(self.create_one, category_data)

    def get_categories(self) -> dict:
        """
        Retrieves all registered categories.
        """
        return self._safe_db_operation(self.get_all)

    def get_category_by_id(self, category_id: str) -> Optional[dict]:
        """
        Retrieves a category by ID.
        """
        try:
            result = self._safe_db_operation(self.get_one_by_id, ObjectId(category_id))
            return Reusable().convert_objectid_to_str(result) if result else None
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving category by ID: {str(e)}")

    def update_category(self, category_id: str, category_data: dict, file: Optional[UploadFile] = None) -> dict:
        """
        Updates a category's data by ID.
        """
        try:
            file_data = {file.filename: file} if file else {}
            result = self._safe_db_operation(self.update_one, ObjectId(category_id), category_data, file_data)
            return Reusable().convert_objectid_to_str(result) if result else None
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating category: {str(e)}")

    def delete_category(self, category_id: str) -> dict:
        """
        Soft deletes a category by ID.
        """
        try:
            result = self._safe_db_operation(self.delete_one, ObjectId(category_id))
            return {"success": True, "msg": "Category successfully deleted"} if result else None
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting category: {str(e)}")
