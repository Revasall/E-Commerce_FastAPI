from typing import List
from fastapi import APIRouter, status, Depends

from backend.app.api.deps import UserDep, allow_admin

from ..schemas.order_sсheme import OrderRead, OrderWithPaymentResponce
from ..services.order_service import OrderServiceDep

router = APIRouter(prefix='/orders', tags=['Order'])

@router.post(
        '/create', 
        response_model=OrderWithPaymentResponce,
        summary="Create a new order",
        status_code=status.HTTP_201_CREATED
        )
async def create_order(current_user: UserDep,
                       service: OrderServiceDep):
    """Convert current cart items into a pending order and generate a payment link."""
    
    return await service.create_order(current_user.id)


@router.get(
        '/',
        summary="Get order history"
        )
async def get_all_order(current_user: UserDep, service: OrderServiceDep):
    """Retrieve a list of all orders placed by the current user."""
    
    return await service.get_all_orders(current_user.id)

@router.get(
        '/{order_id}', 
        response_model=OrderRead,
        summary="Get order details",
        responses={404: {"description": "Order not found"}})
async def get_order_by_id(current_user: UserDep, 
                          service: OrderServiceDep,
                          order_id: int):
    """Fetch detailed information about a specific order by its ID."""
    
    return await service.get_order_by_id(order_id)