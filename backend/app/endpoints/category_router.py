from typing import List
from fastapi import APIRouter, status

from ..schemas.category_sсheme import CategoryRead, CategoryCreate, CategoryUpdate
from ..services.category_service import CategoryServiceDep

router = APIRouter(prefix='/categories', tags=['Categories'])

@router.post('/', response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate,
    service: CategoryServiceDep
    ):

    return await service.create(category_data)

@router.get('/',response_model=List[CategoryRead])
async def get_all_categories(
    service: CategoryServiceDep
    ):

    return await service.get_all()

@router.get('/{category_id}', response_model=CategoryRead)
async def get_category_by_id(
    category_id: int, 
    service: CategoryServiceDep
    ):

    return await service.get_by_id(category_id)

@router.get('/{category_slug}', response_model=CategoryRead)
async def get_category_by_slug(
    category_slug: str, 
    service: CategoryServiceDep
    ):
    
    return await service.get_by_slug(category_slug)

@router.put('/{category_id}', response_model=CategoryRead)
async def update_category(
    category_id: int,
    update_data: CategoryUpdate,
    service: CategoryServiceDep
    ):


    return await service.update(category_id=category_id, category_data=update_data)

@router.delete('/{category_id}', response_model=CategoryRead)
async def delete_category(
    category_id: int,
    service: CategoryServiceDep
    ):

    return await service.delete(category_id)