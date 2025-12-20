
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

from ..models.order import OrderStatus 



class OrderItemBase(BaseModel):
    product_name: str = Field(max_length=30)
    price: float = Field(gt=0)
    quantity: int = Field(gt=1)

class OrderItemCreate(OrderItemBase):
    order_id: int
    product_id: int

class OrderItemRead(OrderItemBase):
    id: int
    product_id: int

    model_config = ConfigDict(from_attributes=True)


class OrderBase(BaseModel):
    user_id: int
    status: OrderStatus = OrderStatus.PENDING

    total_quantity: int
    total_price: float = Field(gt=0)

class OrderCreate(OrderBase):
    ...

class OrderRead(OrderBase):
    id: int
    created_at: datetime
    items: list[OrderItemRead]

    model_config = ConfigDict(from_attributes=True)

class OrderUpdate(BaseModel):
    status: OrderStatus | None = None 
