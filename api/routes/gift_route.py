from fastapi import APIRouter, HTTPException, Depends, UploadFile, status, Form, File
from typing import List, Optional
from models.gift_model import GiftCreate, GiftUpdate, GiftsResponse
from controllers.gift_controller import GiftController

# Router for gift-related endpoints
router = APIRouter()

def parse_gift(
    name: str = Form(...),
    price: float = Form(...),
    payment_url: str = Form(...),
    category: str = Form(...),
) -> GiftCreate:
    return GiftCreate(name=name, price=price, payment_url=str(payment_url), category=category)


# Route: Create a new gift (admin-only)
@router.post("/gifts", response_model=GiftsResponse)
async def create_gift(
    gift: GiftCreate = Depends(parse_gift),
    photo: Optional[UploadFile] = File(None, description="Upload one files."),
    controller: GiftController = Depends(lambda: GiftController()),
):

    return controller.create_gift(gift.dict(), photo)

# Route: Retrieve all gifts (admin-only)
@router.get("/gifts", response_model=GiftsResponse)
async def get_gifts(
    controller: GiftController = Depends(lambda: GiftController()),
):
    return controller.get_gifts()

# Route: Retrieve gift by ID
@router.get("/gifts/{gift_id}", response_model=GiftsResponse)
async def get_gift_by_id(
    gift_id: str,
    controller: GiftController = Depends(lambda: GiftController()),
):
    gift = controller.get_gift_by_id(gift_id)
    if not gift:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gift not found")
    return gift

# Route: Update gift
@router.put("/gifts/{gift_id}", response_model=GiftsResponse)
async def update_gift(
    gift_id: str,
    gift: GiftUpdate,
    files: Optional[List[UploadFile]] = None,
    controller: GiftController = Depends(lambda: GiftController()),
):
    return controller.update_gift(gift_id, gift.dict(exclude_unset=True), {file.filename: file for file in files} if files else {})

# Route: Delete gift (admin-only)
@router.delete("/gifts/{gift_id}", response_model=GiftsResponse)
async def delete_gift(
    gift_id: str,
    controller: GiftController = Depends(lambda: GiftController()),
):
    return controller.delete_gift(gift_id)
