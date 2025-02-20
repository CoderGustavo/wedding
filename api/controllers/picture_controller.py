from .base import BaseClass
from utilities.Reusable import Reusable
from fastapi import HTTPException, UploadFile
from typing import Optional, Dict, List
from datetime import datetime
import copy

class PictureController(BaseClass):
    def __init__(self):
        """
        Initializes the PictureController by defining the specific MongoDB collection.
        """
        super().__init__()
        self.collection_name = "pictures"  # Nome da coleção no MongoDB

    def upload_pictures(self, picture_data: dict, pictures: Optional[list[UploadFile]] = None) -> dict:
        """
        Faz o upload de novas imagens para o Cloudflare R2 e armazena seus metadados no MongoDB.
        """
        if not pictures:
            raise HTTPException(status_code=400, detail="Envie pelo menos uma foto.")

        pictures_data = []

        for picture in pictures:
            if picture.content_type and picture.content_type.startswith("image/"):
                new_picture_data = copy.deepcopy(picture_data)
                uploaded_image_url = self._upload_image(picture)
                new_picture_data["picture"] = uploaded_image_url
                pictures_data.append(new_picture_data)

        if len(pictures_data) <= 0:
            raise HTTPException(status_code=400, detail="Só é permitido o envio de imagens.")

        pictures_uploaded = []

        for data in pictures_data:
            pictures_uploaded.append(self._safe_db_operation(self.create_one, data).get(self.collection_name)[0])

        return {self.collection_name: pictures_uploaded}


    def get_pictures(self) -> List[dict]:
        """
        Retorna metadados de todas as imagens.
        """
        try:
            pictures = self._safe_db_operation(self.get_all)
            return Reusable().convert_objectid_to_str(pictures) if pictures else None
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving pictures: {str(e)}")

    def get_picture_by_id(self, picture_id: str) -> Optional[dict]:
        """
        Retorna metadados de uma imagem pelo ID.
        """
        try:
            picture = self._safe_db_operation(self.get_one_by_id, picture_id)
            if picture:
                return picture[self.collection_name][0]
            raise HTTPException(status_code=404, detail="Picture not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving picture by ID: {str(e)}")

    def update_picture(self, picture_id: str, picture_data: dict, files: Optional[Dict[str, UploadFile]] = None) -> dict:
        """
        Atualiza metadados de uma imagem, substituindo o arquivo, se necessário.
        """
        try:
            if files and isinstance(files, dict):
                for filename, file in files.items():
                    # Fazer o upload da nova imagem e atualizar os dados
                    file_url = self._upload_image(file)
                    picture_data.update({
                        "filename": filename,
                        "content_type": file.content_type,
                        "size": file.file.__sizeof__(),
                        "last_update_date": datetime.utcnow(),
                        "url": file_url,
                    })
            result = self._safe_db_operation(self.update_one, picture_id, picture_data, {})
            return result[self.collection_name][0]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating picture: {str(e)}")

    def delete_picture(self, picture_id: str) -> dict:
        """
        Marca uma imagem como deletada.
        """
        try:
            result = self._safe_db_operation(self.delete_one, picture_id)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting picture: {str(e)}")
