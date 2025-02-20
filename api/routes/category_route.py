from fastapi import APIRouter, HTTPException, Depends, UploadFile, status, Form
from typing import List, Optional
from models.category_model import CategoryCreate, CategoryUpdate, CategoriesResponse
from controllers.category_controller import CategoryController

# Router for category-related endpoints
router = APIRouter()

def parse_category(
    name: str = Form(...)
) -> CategoryCreate:
    return CategoryCreate(name=name)


# Route: Create a new category (admin-only)
@router.post("/categories", response_model=CategoriesResponse)
async def create_category(
    category: CategoryCreate = Depends(parse_category),
    image: Optional[UploadFile] = None,
    controller: CategoryController = Depends(lambda: CategoryController()),
):
    return controller.create_category(category.dict(), image)

# Route: Retrieve all categories
@router.get("/categories", response_model=CategoriesResponse)
async def get_categories(
    controller: CategoryController = Depends(lambda: CategoryController()),
):
    return controller.get_categories()

# Route: Retrieve category by ID
@router.get("/categories/{category_id}", response_model=CategoriesResponse)
async def get_category_by_id(
    category_id: str,
    controller: CategoryController = Depends(lambda: CategoryController()),
):
    category = controller.get_category_by_id(category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category

# Route: Update category
@router.put("/categories/{category_id}", response_model=CategoriesResponse)
async def update_category(
    category_id: str,
    category: CategoryUpdate,
    file: Optional[UploadFile] = None,
    controller: CategoryController = Depends(lambda: CategoryController()),
):
    return controller.update_category(category_id, category.dict(exclude_unset=True), file)

# Route: Delete category (admin-only)
@router.delete("/categories/{category_id}", response_model=CategoriesResponse)
async def delete_category(
    category_id: str,
    controller: CategoryController = Depends(lambda: CategoryController()),
):
    return controller.delete_category(category_id)
