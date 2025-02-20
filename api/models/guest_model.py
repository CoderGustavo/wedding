from pydantic import BaseModel, Field, validator
from typing import List
from utilities.Reusable import Reusable


class GuestCreate(BaseModel):
    """
    Modelo para criação de uma novo convidado.
    """
    name: str = Field(..., min_length=3, description="Nome do convidado")
    phone: str = Field(..., description="Telefone do convidado")
    minor: bool = Field(..., description="Convidado é menor de idade")
    role: str = Field(..., description="Função do convidado")

    @validator('phone', pre=True)
    def validate_and_format_phone(cls, v):
        return Reusable().format_phone_number(v)


class GuestsExpected(BaseModel):
    """
    Modelo esperado para um convidado.
    """
    name: str = Field(..., description="Nome do convidado")
    phone: str = Field(..., description="Telefone do convidado")
    minor: bool = Field(False, description="Convidado é menor de idade")
    role: str = Field(..., description="Função do convidado")

    @validator('phone', pre=True)
    def validate_and_format_phone(cls, v):
        return Reusable().format_phone_number(v)

class GuestUpdate(BaseModel):
    """
    Modelo para atualização de um convidado existente.
    """
    name: str = Field(..., description="Nome do convidado")
    phone: str = Field(..., description="Telefone do convidado")
    minor: bool = Field(..., description="Convidado é menor de idade")
    role: str = Field(..., description="Função do convidado")

    @validator('phone', pre=True)
    def validate_and_format_phone(cls, v):
        return Reusable().format_phone_number(v)

class GuestResponse(BaseModel):
    """
    Modelo de resposta para exibição de dados do convidado.
    """
    id: str = Field(..., description="Identificador único do convidado no banco")
    name: str = Field("Desconhecido", description="Nome do convidado")
    phone: str = Field("(00) 00000-0000", description="Telefone do convidado")
    minor: bool = Field(False, description="Convidado é menor de idade")
    role: str = Field("guest", description="Função do convidado")
    confirmed: bool = Field(False, description="Convidado confirmou presença no periodo atual")

    @validator('phone', pre=True)
    def validate_and_format_phone(cls, v):
        return Reusable().format_phone_number(v)

    class Config:
        """
        Configurações do modelo.
        """
        from_attributes = True  # Permite o uso com objetos retornados por ORMs

class GuestsResponse(BaseModel):
    guests: List[GuestResponse]

