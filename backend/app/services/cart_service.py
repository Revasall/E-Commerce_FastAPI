from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.cart import Cart
from backend.app.repository.cart_repository import CartRepository
from backend.app.repository.product_repository import ProductRepository

from ..schemas.cart_sсheme import CartItemCreate, CartItemRead, CartItemUpdate, CartScheme
from ..core.exceptions import ObjectNotFoundError
from ..database.database import SessionDep

class CartService:

    def __init__(self, db: AsyncSession):
        self.repository = CartRepository(db)
        self.product_repository = ProductRepository(db)

    async def _build_cart_responce(self, cart: Cart) -> CartScheme:
        items = await self.repository.get_cart_items(cart.id)
        if items: 
            cart_items_read = []
            for item in items:
                item.total_price = item.quantity * item.price
                cart_items_read.append(CartItemRead.model_validate(item))
            total_quantity = sum(item.quantity for item in items)
            total_price = sum(item.price * item.quantity for item in items)
        else: 
            cart_items_read, total_quantity, total_price = [], 0, 0

        return CartScheme(
            id=cart.id,
            user_id=cart.user_id,
            items=cart_items_read,
            total_quantity=total_quantity,
            total_price=total_price
        )
    
    async def _check_cart(self, user_id: int) -> Cart:
        cart = await self.repository.get_cart_by_user_id(user_id)
        if not cart:
            raise ObjectNotFoundError('Cart')
        return cart


    async def get_cart(self, user_id:int) -> CartScheme:
        """Get cart by user_id or create if cart doesn't exist"""
        cart = await self.repository.get_cart_by_user_id(user_id)
        if not cart:
            cart = await self.repository.create_cart(user_id)
        return await self._build_cart_responce(cart)
    
    async def add_item(self, user_id:int, item_data: CartItemCreate) -> CartScheme:

        product = await self.product_repository.get_by_id(item_data.product_id)
        if not product:
            raise ObjectNotFoundError('Product')
        
        cart = await self.repository.get_cart_by_user_id(user_id)
        if not cart:
            cart = await self.repository.create_cart(user_id)

        existing_item = await self.repository.get_item(cart_id=cart.id, product_id= product.id)
        if existing_item:
            existing_item.quantity += item_data.quantity
            await self.repository.db.commit()
            await self.repository.db.refresh(existing_item)
        else:
            item_data.cart_id = cart.id
            item = await self.repository.add_item(item_data)

        #Reload cart from DB 
        cart = await self.repository.get_cart_by_user_id(user_id)
        
        return await self._build_cart_responce(cart)
    
    async def update_item(self, 
                          user_id: int, 
                          item_id:int, 
                          item_update_data: CartItemUpdate) -> CartScheme:

        cart = await self._check_cart(user_id)

        item = await self.repository.update_item_quantity(item_id, item_update_data.quantity)
        if not item: 
            raise ObjectNotFoundError('Item')
        return await self._build_cart_responce(cart)
    
    async def remove_item(self, user_id:int, item_id: int) -> CartScheme: 
        cart = await self._check_cart(user_id)

        remove = await self.repository.remove_item(item_id)
        if not remove:
            raise ObjectNotFoundError('Item')
        
        return await self._build_cart_responce(cart)

    async def clear_cart(self, user_id: int) -> CartScheme:
        cart = await self._check_cart(user_id)    

        result = await self.repository.clear_cart(cart.id)
        if not result: 
            raise ObjectNotFoundError('Items')
    
        
        return await self._build_cart_responce(cart)
        
def get_cart_service(session: SessionDep):
    return CartService(session)

CartServiceDep = Annotated[CartService, Depends(get_cart_service)]
