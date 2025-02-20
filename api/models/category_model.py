from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from datetime import datetime

class CategoryCreate(BaseModel):
    """
    Modelo para criação de uma nova categoria.
    """
    name: str = Field(..., description="Nome da categoria")

class CategoryExpected(BaseModel):
    """
    Modelo esperado para uma categoria.
    """
    name: str = Field(..., description="Nome da categoria")
    image: str = Field(..., description="Caminho ou URL da imagem da categoria")


class CategoryUpdate(BaseModel):
    """
    Modelo para atualização de uma categoria existente.
    """
    name: Optional[str] = Field(None, description="Nome atualizado da categoria")
    image: Optional[str] = Field(None, description="Caminho ou URL atualizado da imagem da categoria")

class CategoryResponse(BaseModel):
    """
    Modelo de resposta para exibição de dados da categoria.
    """
    id: str = Field(..., description="Identificador único da categoria no banco")
    name: str = Field("Desconhecido", description="Nome da categoria")
    image: str = Field("https://teste.com", description="Caminho ou URL da imagem associada à categoria")

    class Config:
        """
        Configurações do modelo.
        """
        from_attributes = True  # Permite o uso com objetos retornados por ORMs

class CategoriesResponse(BaseModel):
    categories: List[CategoryResponse]
