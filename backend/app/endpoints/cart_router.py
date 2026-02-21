from typing import List
from fastapi import APIRouter, status, Depends

from backend.app.api.deps import UserDep, allow_admin

from ..schemas.cart_sсheme import CartItemCreate, CartItemUpdate, CartScheme
from ..services.cart_service import CartServiceDep

router = APIRouter(prefix='/cart', tags=['Cart'])

@router.get('/', response_model=CartScheme)
async def get_cart(current_user: UserDep, service: CartServiceDep):
    return await service.get_cart(current_user.id)

@router.post('/items', response_model=CartScheme)
async def add_item(current_user: UserDep, 
                   service: CartServiceDep,
                   item_data: CartItemCreate):
    
    return await service.add_item(current_user.id, item_data)

@router.put('/items/{item_id}', response_model=CartScheme)
async def update_cart(current_user: UserDep,
                      service: CartServiceDep,
                      item_id: int,
                      item_data: CartItemUpdate):
    
    return await service.update_item(current_user.id, item_id, item_data)

@router.delete('/items/{item_id}', response_model=CartScheme)
async def remove_item(current_user: UserDep,
                      service: CartServiceDep,
                      item_id: int):
    
    return await service.remove_item(current_user.id, item_id)

@router.delete('/clear', response_model=CartScheme)
async def clear_cart(current_user: UserDep,
                     service: CartServiceDep):
    
    return await service.clear_cart(current_user.id)