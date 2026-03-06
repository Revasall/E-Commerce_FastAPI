from typing import List
from fastapi import APIRouter, status, Depends

from ..api.deps import UserDep, allow_admin

from ..schemas.category_sсheme import CategoryRead, CategoryCreate, CategoryUpdate
from ..services.category_service import CategoryServiceDep

router = APIRouter(prefix='/categories', tags=['Categories'])

@router.post(
        '/', 
        response_model=CategoryRead, 
        status_code=status.HTTP_201_CREATED, 
        dependencies=[Depends(allow_admin)],
        summary="Create a category (Admin only)"
        )
async def create_category(
    current_user: UserDep, # Used for admin check in dependencies
    category_data: CategoryCreate,
    service: CategoryServiceDep,
    ):
    """Creates a new product category. Requires administrative privileges."""
    
    return await service.create(category_data)

@router.get(
        '/',
        response_model=List[CategoryRead],
        summary="Get all categories"
        )
async def get_all_categories(
    service: CategoryServiceDep
    ):
    """Returns a complete list of all available product categories."""

    return await service.get_all()

@router.get(
        '/id/{category_id}', 
        response_model=CategoryRead,
        summary="Get category by ID")
async def get_category_by_id(
    category_id: int, 
    service: CategoryServiceDep
    ):
    """Fetch a specific category using its unique integer ID."""

    return await service.get_by_id(category_id)

@router.get(
        '/{category_slug}', 
        response_model=CategoryRead,
        summary="Get category by slug"
        )
async def get_category_by_slug(
    category_slug: str, 
    service: CategoryServiceDep
    ):
    """Fetch a specific category using its URL-friendly slug."""
    
    return await service.get_by_slug(category_slug)

@router.put(
        '/id/{category_id}', 
        response_model=CategoryRead, 
        dependencies=[Depends(allow_admin)],
        summary="Update category (Admin only)")
async def update_category(
    current_user: UserDep,
    category_id: int,
    update_data: CategoryUpdate,
    service: CategoryServiceDep
    ):
    """Updates category attributes. Restricted to administrators."""

    return await service.update(category_id=category_id, category_data=update_data)

@router.delete(
        '/id/{category_id}', 
        response_model=CategoryRead, 
        dependencies=[Depends(allow_admin)],
        summary="Delete category (Admin only)")
async def delete_category(
    current_user: UserDep,
    category_id: int,
    service: CategoryServiceDep
    ):
    """Removes a category from the database. Restricted to administrators."""
    
    return await service.delete(category_id)