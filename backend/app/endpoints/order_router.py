from fastapi import APIRouter, Request, status

from ..api.deps import UserDep

from ..schemas.order_sсheme import OrderRead, OrderWithPaymentResponce
from ..services.order_service import OrderServiceDep
from ..core.limiter import limiter

router = APIRouter(prefix='/orders', tags=['Orders'])

@router.post(
        '/create', 
        response_model=OrderWithPaymentResponce,
        summary="Create a new order",
        status_code=status.HTTP_201_CREATED
        )
@limiter.limit('3/minute')
async def create_order(request: Request,
                       current_user: UserDep,
                       service: OrderServiceDep):
    """Convert current cart items into a pending order and generate a payment link."""
    
    return await service.create_order(current_user.id)


@router.get(
        '/',
        summary="Get order history"
        )
@limiter.limit('20/minute')
async def get_all_order(
    request: Request,
    current_user: UserDep, 
    service: OrderServiceDep
    ):
    """Retrieve a list of all orders placed by the current user."""
    
    return await service.get_all_orders(current_user.id)

@router.get(
        '/{order_id}', 
        response_model=OrderRead,
        summary="Get order details",
        responses={404: {"description": "Order not found"}})
@limiter.limit('20/minute')
async def get_order_by_id(current_user: UserDep, 
                          service: OrderServiceDep,
                          order_id: int,
                          request: Request):
    """Fetch detailed information about a specific order by its ID."""
    
    return await service.get_order_by_id(order_id)