from fastapi import APIRouter, HTTPException, Depends, status, Form, UploadFile
from typing import Optional

from models.guest_model import GuestCreate, GuestUpdate, GuestsResponse
from controllers.guest_controller import GuestController
from utilities.Reusable import Reusable

# Router for guest-related endpoints
router = APIRouter()

def parse_guest(
    name: str = Form(...),
    phone: str = Form(...),
    minor: bool = Form(...),
    role: str = Form(...),
) -> GuestCreate:
    return GuestCreate(name=name, phone=phone, minor=minor, role=role)


# Route: Create a new guest
@router.post("/guests", response_model=GuestsResponse)
async def create_guest(
    guest: GuestCreate = Depends(parse_guest),
    controller: GuestController = Depends(lambda: GuestController()),
):

    return controller.create_guest(guest.dict())

# Route: Retrieve all guests (admin-only)
@router.get("/guests", response_model=GuestsResponse)
async def get_guests(
    controller: GuestController = Depends(lambda: GuestController()),
):
    return controller.get_guests()

# Route: Retrieve guest by ID
@router.get("/guests/{guest_id}", response_model=GuestsResponse)
async def get_guest_by_id(
    guest_id: str,
    controller: GuestController = Depends(lambda: GuestController()),
):
    guest = controller.get_guest_by_id(guest_id)
    if not guest:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Guest not found")
    return guest

# Route: Retrieve guest by phone
@router.get("/guests/phone/{phone}", response_model=GuestsResponse)
async def get_guests_by_phone(
    phone: str,
    controller: GuestController = Depends(lambda: GuestController()),
):
    try:
        phone = Reusable().format_phone_number(phone)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    guest = controller.get_guests_by_phone(phone)
    if not guest:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Guest not found")
    return guest

# Route: Update guest
@router.put("/guests/{guest_id}", response_model=GuestsResponse)
async def update_guest(
    guest_id: str,
    guest: GuestUpdate,
    files: Optional[list[UploadFile]] = None,
    controller: GuestController = Depends(lambda: GuestController()),
):
    return controller.update_guest(guest_id, guest.dict(exclude_unset=True), {file.filename: file for file in files} if files else {})

# Route: Delete guest (admin-only)
@router.delete("/guests/{guest_id}", response_model=dict)
async def delete_guest(
    guest_id: str,
    controller: GuestController = Depends(lambda: GuestController()),
):
    return controller.delete_guest(guest_id)
