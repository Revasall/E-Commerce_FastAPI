from typing import List
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.order import Order, OrderItem
from ..schemas.cart_sсheme import CartItemCreate