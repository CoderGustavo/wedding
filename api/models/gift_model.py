from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

class GiftCreate(BaseModel):
    """
    Modelo para criação de presente.
    """
    name: str = Field(..., description="Nome do presente")
    price: float = Field(..., ge=0, description="Preço do presente (em moeda local)")
    payment_url: HttpUrl = Field(..., description="Link de pagamento do presente")
    category: str = Field(..., description="Categoria do presente")

class GiftExpected(BaseModel):
    """
    Modelo para criação de uma nova entrada de presente.
    """
    name: str = Field(..., description="Nome do presente")
    price: float = Field(..., ge=0, description="Preço do presente (em moeda local)")
    payment_url: HttpUrl = Field(..., description="Link de pagamento do presente")
    category: str = Field(..., description="Categoria do presente")
    image: str = Field(..., description="Caminho ou URL da imagem do presente")


class GiftUpdate(BaseModel):
    """
    Modelo para atualização de metadados de um presente existente.
    """
    name: Optional[str] = Field(None, description="Nome atualizado do presente")
    price: Optional[float] = Field(None, ge=0, description="Preço atualizado do presente (em moeda local)")
    payment_url: Optional[HttpUrl] = Field(None, description="Link atualizado de pagamento do presente")
    image: Optional[str] = Field(None, description="Caminho ou URL atualizado da imagem do presente")
    category: Optional[str] = Field(None, description="Categoria atualizada do presente")

class GiftResponse(BaseModel):
    """
    Modelo de resposta para exibição de dados do presente.
    """
    id: str = Field(..., description="Identificador único do presente no banco")
    name: str = Field("Desconhecido", description="Nome do presente")
    price: float = Field(0, description="Preço do presente (em moeda local)")
    payment_url: HttpUrl = Field("https://teste.com", description="Link de pagamento do presente")
    image: str = Field("https://teste.com", description="Caminho ou URL da imagem associada ao presente")
    category: str = Field("Desconhecido", description="Categoria do presente")
    deleted: str = Field(False, description="If the gift was deleted or not")

    class Config:
        """
        Configurações do modelo.
        """
        from_attributes = True  # Permite o uso com objetos retornados por ORMs

class GiftsResponse(BaseModel):
    gifts: List[GiftResponse]

