from typing import List
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models.cart import Cart, CartItem
from ..schemas.cart_sсheme import CartItemCreate

class CartRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_cart(self, user_id:int)-> Cart:
        cart = Cart(user_id=user_id)
        self.db.add(cart)
        await self.db.commit()
        await self.db.refresh(cart)
        return cart
    
    async def get_cart_by_user_id(self, user_id:int) -> Cart:
        cart = await self.db.scalar(select(Cart).where(Cart.user_id == user_id))
        return cart
    
    async def add_item(self, item_data: CartItemCreate)->CartItem:
        cart_item = CartItem(**item_data.model_dump())
        self.db.add(cart_item)
        await self.db.commit()
        await self.db.refresh(cart_item)
        return cart_item
    
    async def get_item(self, cart_id:int, product_id: int) -> CartItem:
        result = await self.db.scalar(select(CartItem).where(CartItem.cart_id == cart_id, CartItem.product_id ==product_id))
        return result
    
    async def get_item_by_id(self, item_id: int)-> CartItem:
        result = await self.db.scalar(select(CartItem).where(CartItem.id == item_id))
        return result
    
    async def update_item_quantity(self, item_id:int, quantity:int) -> CartItem|None:
        item = await self.get_item_by_id(item_id=item_id)
        if item:
            item.quantity = quantity
            await self.db.commit()
            await self.db.refresh(item)
        return item 
    
    async def remove_item(self, item_id:int) -> bool:
        item = await self.get_item_by_id(item_id)
        if item:
            await self.db.delete(item)
            await self.db.commit()
            return True
        return False
    
    async def clear_cart(self, cart_id:int) -> bool:
        result = await self.db.execute(delete(CartItem).where(CartItem.cart_id == cart_id))
        await self.db.commit()
        
        return result.rowcount > 0

    async def get_cart_items(self, cart_id: int) -> List[CartItem]:
        result = await self.db.execute(select(CartItem).options(selectinload(CartItem.product)).where(CartItem.cart_id==cart_id))
        return list(result.scalars().all())