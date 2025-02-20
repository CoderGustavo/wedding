from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class ConfirmationCreate(BaseModel):
    """
    Modelo para criação de uma nova confirmação
    """
    guest_id: str = Field(..., description="ID do convidado associado")
    confirmed: bool = Field(False, description="Status de confirmação (ex: 'confirmado', 'pendente', 'recusado')")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Datetime de quanto foi criado a confirmação")

class ConfirmationExpected(BaseModel):
    """
    Modelo esperado para uma confirmação
    """
    guest_id: str = Field(..., description="ID do convidado associado")
    confirmed: bool = Field(False, description="Status de confirmação")

class ConfirmationUpdate(BaseModel):
    """
    Modelo para atualização de uma confirmação existente
    """
    guest_id: str = Field(..., description="ID do convidado associado")
    confirmed: bool = Field(False, description="Status de confirmação atualizado")

class ConfirmationResponse(BaseModel):
    """
    Modelo de resposta para exibição de dados de confirmação
    """
    id: str = Field(..., description="Identificador único da confirmação")
    guest_id: str = Field(..., description="ID do convidado associado")
    confirmed: bool = Field(False, description="Status atual da confirmação")
    created_at: datetime = Field(None, description="Data de criação da confirmação")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "guest_id": "6587c8a8d14d4472b6e785a2",
                "confirmed": False,
                "created_at": "2023-12-25T10:30:00Z"
            }
        }

class ConfirmationsResponse(BaseModel):
    """
    Modelo de resposta para lista de confirmações
    """
    confirmations: List[ConfirmationResponse]