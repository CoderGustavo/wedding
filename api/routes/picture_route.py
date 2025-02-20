from fastapi import APIRouter, HTTPException, Depends, UploadFile, status, Form, File
from typing import List, Optional
from controllers.picture_controller import PictureController
from models.picture_model import PicturesResponse, PictureCreate

# Router for picture-related endpoints
router = APIRouter()

def parse_picture(
    guest_name: str = Form(...),
) -> PictureCreate:
    return PictureCreate(guest_name=guest_name)


# Route: Upload a new picture
@router.post("/pictures", response_model=PicturesResponse)
async def upload_picture(
    guest_name: PictureCreate = Depends(parse_picture),
    files: List[UploadFile] = File(None, description="Upload one files."),
    controller: PictureController = Depends(lambda: PictureController()),
):
    """
    Uploads one or more pictures to the server.
    """

    return controller.upload_pictures(guest_name.dict(), files)

# Route: Retrieve all pictures
@router.get("/pictures", response_model=PicturesResponse)
async def get_pictures(
    controller: PictureController = Depends(lambda: PictureController()),
):
    """
    Retrieves metadata for all uploaded pictures.
    """
    return controller.get_pictures()

# Route: Retrieve picture by ID
@router.get("/pictures/{picture_id}", response_model=PicturesResponse)
async def get_picture_by_id(
    picture_id: str,
    controller: PictureController = Depends(lambda: PictureController()),
):
    """
    Retrieves a picture's metadata by ID.
    """
    picture = controller.get_picture_by_id(picture_id)
    if not picture:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Picture not found")
    return picture

# Route: Update picture metadata
@router.put("/pictures/{picture_id}", response_model=PicturesResponse)
async def update_picture(
    picture_id: str,
    metadata: PicturesResponse,
    controller: PictureController = Depends(lambda: PictureController()),
):
    """
    Updates metadata for a picture by ID.
    """
    updated_picture = controller.update_picture(picture_id, metadata)
    if not updated_picture:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Picture not found")
    return updated_picture

# Route: Delete picture by ID
@router.delete("/pictures/{picture_id}", response_model=PicturesResponse)
async def delete_picture(
    picture_id: str,
    controller: PictureController = Depends(lambda: PictureController()),
):
    """
    Deletes a picture by ID.
    """
    result = controller.delete_picture(picture_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Picture not found")
    return {"success": True, "message": "Picture successfully deleted"}
