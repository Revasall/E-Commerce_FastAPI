from typing import List
from fastapi import APIRouter, status

from ..schemas.product_sсheme import ProductRead, ProductCreate, ProductUpdate
from ..services.product_service import ProductServiceDep


router = APIRouter(prefix='/products', tags=['Products'])

@router.post('/', response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    service:ProductServiceDep
):
    
    return await service.create(product_data)

@router.get('/', response_model=List[ProductRead])
async def get_all_products(
    service: ProductServiceDep
):
    
    return await service.get_all_products()

@router.get('/{product_id}', response_model=ProductRead)
async def get_product_by_id(
    product_id: int,
    service: ProductServiceDep
):
    return await service.get_by_id(product_id)

@router.put('/{product_id}', response_model=ProductRead)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    service: ProductServiceDep):

    return await service.update_product(product_id, product_data)

@router.delete('/{product_id}', response_model=ProductRead)
async def delete_product(
    product_id: int,
    service: ProductServiceDep
    ):

    return await service.delete_product(product_id)
