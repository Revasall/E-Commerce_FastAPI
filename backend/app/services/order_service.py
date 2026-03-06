from datetime import datetime, timezone

from fastapi import Depends
from typing import Annotated, Any, List
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.order import Order, OrderStatus
from ..repository.order_repository import OrderRepository
from ..repository.cart_repository import CartRepository
from ..services.cart_service import CartService

from ..services.payment.yookassa_provider import YookassaProvider

from ..schemas.cart_sсheme import CartItemCreate, CartItemRead, CartItemUpdate, CartScheme
from ..schemas.order_sсheme import OrderCreate, OrderItemCreate, OrderItemRead, OrderRead, OrderUpdate, OrderWithPaymentResponce

from ..core.exceptions import ObjectNotFoundError, ObjectCreateError
from ..database.database import SessionDep
from ..core.utils import ensure_exists

class OrderService:
    """
    Main business logic layer for order management.
    Handles the transition from shopping cart to order and integrates with payment providers.
    """

    def __init__(self, db: AsyncSession):
        self.repository = OrderRepository(db)
        self.cart_service = CartService(db)
        self.payment_provider = YookassaProvider()

    async def _build_order_response(self, order: Order|None) -> OrderRead:
        """
        Private helper to enrich Order model with its items for a detailed response.
        """

        if not order:
            raise ObjectNotFoundError('Order')
        
        items = await self.repository.get_order_items(order.id)
        items_read = [OrderItemRead.model_validate(item) for item in items]

        return OrderRead(
            id=order.id,
            user_id=order.user_id,
            status=order.status,
            total_quantity=order.total_quantity,
            total_price=order.total_price,
            created_at=order.created_at,
            items=items_read,
            external_id=order.external_id,
            paid_at=order.paid_at
            )
    
    async def create_order(self, user_id: int) -> OrderWithPaymentResponce:
        """
        Converts a user's active cart into a formal order.
        
        Steps:
        1. Fetch and validate cart content.
        2. Create order and order items records.
        3. Generate a payment link via Yookassa.
        4. Clear the cart upon successful order creation.
        """

        cart = await self.cart_service.get_cart(user_id)
        if not cart:
            raise ObjectNotFoundError('Cart')
        
        # Map cart items to order item creation schemas (capturing current price snapshots)
        items = [
            OrderItemCreate(
                product_id=item.product_id,
                product_name=item.product_title,
                price=item.price,
                quantity=item.quantity,
                result_price=item.total_price
            ) for item in cart.items]
        if len(items) == 0:
            raise ObjectNotFoundError('Items')
        
        order = OrderCreate(
            user_id = user_id,
            total_quantity=cart.total_quantity,
            total_price=cart.total_price,
            items=items
        )
        
        order = await self.repository.create_order(order)
        if not order:
            raise ObjectCreateError('Order')
        
        
        # Generate payment session
        payment_url, payment_id = await self.payment_provider.create_payment_link(order)

        # Link payment provider's ID to our order
        order = await self.repository.update_order(order.id, OrderUpdate(
            external_id=payment_id
        ))

        await self.cart_service.clear_cart(user_id)

        return OrderWithPaymentResponce(
            order = await self._build_order_response(order), 
            payment_url = payment_url)
    
    
    async def get_all_orders(self, user_id:int) -> List[OrderRead]:
        """Retrieves a specific order with full item details."""

        result = await self.repository.get_all_orders_by_user_id(user_id)
        
        if result == []:
            raise ObjectNotFoundError('Orders')
        
        orders_list = []
        for order in result:
            read_order = OrderRead(
            id=order.id,
            user_id=order.user_id,
            status=order.status,
            total_quantity=order.total_quantity,
            total_price=order.total_price,
            created_at=order.created_at,
            items=[],
            external_id=order.external_id,
            paid_at=order.paid_at
            )
            orders_list.append(read_order)
        
        return orders_list 

    
    async def get_order_by_id(self, order_id: int):
        """Returns the complete order history for a user."""

        order = await self.repository.get_order_by_id(order_id)
        
        return await self._build_order_response(order)
    
    
    async def order_payment_update(self, 
                                   order_id:int,
                                   external_id: str,
                                   payment_details: dict[str, Any]) -> OrderRead:
        """
        Updates order status to PAID after successful webhook notification.
        Records external transaction details and payment timestamp.
        """

        order_update_data = OrderUpdate(
            status=OrderStatus.PAID,
            external_id=external_id,
            payment_details=payment_details,
            paid_at=datetime.now(timezone.utc).replace(tzinfo=None)
        )

        order = await self.repository.update_order(order_id, order_update_data)

        return await self._build_order_response(order)
    
    async def order_failed_update(self, order_id: int) -> OrderRead:
        """Marks an order as failed if payment was rejected."""

        order_update_data = OrderUpdate(status=OrderStatus.FAILED)
        order = await self.repository.update_order(order_id, order_update_data)

        return await self._build_order_response(order)
    
    async def order_cancelled_update(self, order_id: int) -> OrderRead:
        """Marks an order as canceled."""

        order_update_data = OrderUpdate(status=OrderStatus.CANCELLED)
        order = await self.repository.update_order(order_id, order_update_data)

        return await self._build_order_response(order)


def get_order_service(session: SessionDep):
    return OrderService(session)

OrderServiceDep = Annotated[OrderService, Depends(get_order_service)]
