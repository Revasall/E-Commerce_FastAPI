from typing import List
from fastapi import APIRouter, status, Depends

from backend.app.api.deps import UserDep, allow_admin

from ..schemas.order_sсheme import OrderCreate, OrderRead, OrderWithPaymentResponce
from ..services.order_service import OrderServiceDep
from ..schemas.cart_sсheme import CartItemCreate, CartItemUpdate, CartScheme
from ..services.cart_service import CartServiceDep

router = APIRouter(prefix='/orders', tags=['Order'])

@router.post('/create', response_model=OrderWithPaymentResponce)
async def create_order(current_user: UserDep,
                       service: OrderServiceDep):
    
    return await service.create_order(current_user.id)


@router.get('/')
async def get_all_order(current_user: UserDep, service: OrderServiceDep):
    return await service.get_all_orders(current_user.id)

@router.get('/{order_id}', response_model=OrderRead)
async def get_order_by_id(current_user: UserDep, 
                          service: OrderServiceDep,
                          order_id: int):
    
    return await service.get_order_by_id(order_id)