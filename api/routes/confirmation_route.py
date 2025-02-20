from fastapi import APIRouter, HTTPException, Depends, status, Form
from typing import Optional

from models.confirmation_model import (
    ConfirmationCreate, 
    ConfirmationUpdate, 
    ConfirmationsResponse
)
from controllers.confirmation_controller import ConfirmationController

# Router para endpoints relacionados a confirmações
router = APIRouter()

def parse_confirmation(
    guest_id: str = Form(...),
    confirmed: bool = Form(...),
) -> ConfirmationCreate:
    return ConfirmationCreate(guest_id=guest_id, confirmed=confirmed)

# Rota: Criar nova confirmação
@router.post("/confirmations", response_model=ConfirmationsResponse)
async def create_confirmation(
    confirmation: ConfirmationCreate = Depends(parse_confirmation),
    controller: ConfirmationController = Depends(ConfirmationController),
):
    return controller.create_confirmation(confirmation.dict())

# Rota: Listar todas as confirmações
@router.get("/confirmations", response_model=ConfirmationsResponse)
async def get_confirmations(
    controller: ConfirmationController = Depends(ConfirmationController),
):
    return controller.get_confirmations()

# Rota: Buscar confirmação por ID
@router.get("/confirmations/{confirmation_id}", response_model=ConfirmationsResponse)
async def get_confirmation_by_id(
    confirmation_id: str,
    controller: ConfirmationController = Depends(ConfirmationController),
):
    confirmation = controller.get_confirmation_by_id(confirmation_id)
    if not confirmation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Confirmação não encontrada")
    return confirmation

# Rota: Buscar confirmações por ID do convidado
@router.get("/confirmations/guest/{guest_id}", response_model=ConfirmationsResponse)
async def get_confirmations_by_guest_id(
    guest_id: str,
    controller: ConfirmationController = Depends(ConfirmationController),
):
    confirmations = controller.get_confirmations_by_guest_id(guest_id)
    if not confirmations:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhuma confirmação encontrada")
    return confirmations

# Rota: Atualizar confirmação
@router.put("/confirmations/{confirmation_id}", response_model=ConfirmationsResponse)
async def update_confirmation(
    confirmation_id: str,
    confirmation: ConfirmationUpdate,
    controller: ConfirmationController = Depends(ConfirmationController),
):
    return controller.update_confirmation(
        confirmation_id,
        confirmation.dict(exclude_unset=True)
    )

# Rota: Excluir confirmação
@router.delete("/confirmations/{confirmation_id}", response_model=dict)
async def delete_confirmation(
    confirmation_id: str,
    controller: ConfirmationController = Depends(ConfirmationController),
):
    return controller.delete_confirmation(confirmation_id)