from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from ..models.order import Order, OrderItem
from ..schemas.order_sсheme import OrderCreate, OrderUpdate

class OrderRepository:
    """
    Data access layer for orders and order items.
    Manages complex persistence logic involving parent orders and their associated line items.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_order(self, order_data: OrderCreate) -> Order|None:
        """
        Сreates an order along with its items.
        Uses flush() to obtain the order ID before creating OrderItem instances.
        """
        # Create the main order record (excluding items for now)
        order = Order(**order_data.model_dump(exclude={'items'}))
        self.db.add(order)
        # Flush to generate order.id without ending the transaction
        await self.db.flush()

        items = [
            OrderItem(
                order_id = order.id,
                product_id = item.product_id,
                product_name = item.product_name,
                price = item.price,
                quantity = item.quantity,
                result_price = item.result_price
                ) for item in order_data.items
                ]
    
        self.db.add_all(items)

        try:
            await self.db.commit()
        except IntegrityError:
            await self.db.rollback()
            
        await self.db.refresh(order)
        return order
    
    async def get_all_orders_by_user_id(self, user_id: int) -> List[Order]:
        """Returns the order history in list format without displaying the order items."""

        result = await self.db.execute(select(Order).where(Order.user_id == user_id))
        return list(result.scalars().all())
    
    async def get_order_by_id(self, order_id: int) -> Order | None:
        """
        Fetches a detailed order record.
        Uses 'selectinload' to eagerly fetch all associated OrderItems.
        """
        
        order = await self.db.scalar(
            select(Order)
            .where(Order.id == order_id)
            .options(selectinload(Order.items)))
        return order
    
    async def get_order_items(self, order_id: int) -> List[OrderItem]:
        """Returns all items in a specific order."""

        result = await self.db.execute(select(OrderItem).where(OrderItem.order_id == order_id))
        return list(result.scalars().all())
    
    async def get_item(self, order_id:int, product_id: int) -> OrderItem:
        """Returns a specific item from a specific order by product id and order id"""

        result = await self.db.scalar(select(OrderItem).where(OrderItem.order_id == order_id, OrderItem.product_id ==product_id))
        return result
    
    async def get_item_by_id(self, item_id: int)-> OrderItem:
        """Returns a specific item of a specific order by item ID"""

        result = await self.db.scalar(select(OrderItem).where(OrderItem.id == item_id))
        return result
    
    async def update_order(self, order_id: int, update_data: OrderUpdate) -> Order | None:
        """Updating order status and incoming payment data"""
        
        order = await self.db.scalar(select(Order).where(Order.id == order_id))
        if order:
            for key, value in update_data.model_dump(exclude_unset=True).items():
                setattr(order, key, value)
            await self.db.commit()
            await self.db.refresh(order)

        return order