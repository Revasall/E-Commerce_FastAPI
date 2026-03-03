from typing import List
from fastapi import APIRouter

from backend.app.api.deps import UserDep, allow_admin

from ..schemas.cart_sсheme import CartItemCreate, CartItemUpdate, CartScheme
from ..services.cart_service import CartServiceDep

router = APIRouter(prefix='/cart', tags=['Cart'])

@router.get(
        '/', 
        response_model=CartScheme,
        summary="Get user cart"
        )
async def get_cart(current_user: UserDep, service: CartServiceDep):
    """Retrieve the current authenticated user's shopping cart."""
    
    return await service.get_cart(current_user.id)

@router.post(
        '/items', 
        response_model=CartScheme,
        summary="Add item to cart",
        responses={404: {"description": "Product not found"}}
        )
async def add_item(current_user: UserDep, 
                   service: CartServiceDep,
                   item_data: CartItemCreate):
    """Add a product to the cart or increase quantity if it already exists."""
    
    return await service.add_item(current_user.id, item_data)

@router.put(
        '/items/{item_id}', 
        response_model=CartScheme,
        summary="Update item quantity"
        )
async def update_cart(current_user: UserDep,
                      service: CartServiceDep,
                      item_id: int,
                      item_data: CartItemUpdate):
    """Change the quantity of a specific item in the cart."""
    
    return await service.update_item(current_user.id, item_id, item_data)

@router.delete(
        '/items/{item_id}', 
        response_model=CartScheme,
        summary="Remove item from cart")
async def remove_item(current_user: UserDep,
                      service: CartServiceDep,
                      item_id: int):
    """Delete a specific product line from the cart."""
    
    return await service.remove_item(current_user.id, item_id)

@router.delete(
        '/clear', 
        response_model=CartScheme,
        summary="Empty the cart"
        )
async def clear_cart(current_user: UserDep,
                     service: CartServiceDep):
    """Remove all items from the current user's cart."""
    
    return await service.clear_cart(current_user.id)