from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class PictureCreate(BaseModel):
    """
    Modelo para criação de uma nova entrada de imagem.
    """
    guest_name: str = Field(..., description="Nome do convidado associado à imagem")


class PictureUpdate(BaseModel):
    """
    Modelo para atualização de metadados de uma imagem existente.
    """
    guest_name: Optional[str] = Field(None, description="Nome atualizado do convidado")
    picture: Optional[str] = Field(None, description="Nome atualizado do arquivo")


class PictureResponse(BaseModel):
    """
    Modelo de resposta para exibição de dados da imagem.
    """
    id: str = Field(..., description="Identificador único da imagem no banco")
    guest_name: str = Field("Desconhecido", description="Nome do convidado associado à imagem")
    picture: str = Field("https://teste.com", description="Nome do arquivo da imagem")

    class Config:
        """
        Configurações do modelo.
        """
        from_attributes = True  # Permite o uso com objetos retornados por ORMs

class PicturesResponse(BaseModel):
    pictures: list[PictureResponse]
