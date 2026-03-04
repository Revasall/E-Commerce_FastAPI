from typing import List
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models.cart import Cart, CartItem
from ..schemas.cart_sсheme import CartItemCreate

class CartRepository:
    """
    Data access layer for shopping cart operations.
    Handles persistence logic for Carts and CartItems using SQLAlchemy AsyncSession.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_cart(self, user_id:int)-> Cart:
        """Initializes a new empty cart for a specific user."""

        cart = Cart(user_id=user_id)
        self.db.add(cart)
        await self.db.commit()
        await self.db.refresh(cart)
        return cart
    
    async def get_cart_by_user_id(self, user_id:int) -> Cart:
        """
        Retrieves a user's cart. 
        Uses 'selectinload' to eagerly fetch cart items in an async-friendly way.
        """

        cart = await self.db.scalar(
            select(Cart)
            .where(Cart.user_id == user_id)
            .options(selectinload(Cart.items)))
        return cart
    
    async def add_item(self, item_data: CartItemCreate)->CartItem:
        """Persists a new product item into the cart."""

        cart_item = CartItem(**item_data.model_dump())
        self.db.add(cart_item)
        await self.db.commit()
        await self.db.refresh(cart_item)
        return cart_item
    
    async def get_item(self, cart_id:int, product_id: int) -> CartItem:
        """Finds a specific product entry within a given cart."""

        result = await self.db.scalar(select(CartItem).where(CartItem.cart_id == cart_id, CartItem.product_id ==product_id))
        return result
    
    async def get_item_by_id(self, item_id: int)-> CartItem:
        """Retrieves a single CartItem by its primary key."""

        result = await self.db.scalar(select(CartItem).where(CartItem.id == item_id))
        return result
    
    async def update_item_quantity(self, item_id:int, quantity:int) -> CartItem|None:
        """Updates the quantity of an existing cart item and refreshes the instance."""

        item = await self.get_item_by_id(item_id=item_id)
        if item:
            item.quantity = quantity
            await self.db.commit()
            await self.db.refresh(item)
        return item 
    
    async def remove_item(self, item_id:int) -> bool:
        """Deletes an item from the cart. Returns True if successful."""

        item = await self.get_item_by_id(item_id)
        if item:
            await self.db.delete(item)
            await self.db.commit()
            return True
        return False
    
    async def clear_cart(self, cart_id:int) -> Cart | None:
        """
        Removes all items from a cart in a single batch operation.
        Returns the updated cart object with an empty items list.
        """

        result = await self.db.execute(delete(CartItem).where(CartItem.cart_id == cart_id))
        await self.db.commit()
        
        # Rowcount check ensures we only fetch if something was actually deleted
        if result.rowcount > 0:
            cart = await self.db.scalar(select(Cart).where(Cart.id == cart_id))
            return cart
        return None

    async def get_cart_items(self, cart_id: int) -> List[CartItem]:
        result = await self.db.execute(select(CartItem).options(selectinload(CartItem.product)).where(CartItem.cart_id==cart_id))
        return list(result.scalars().all())