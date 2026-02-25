
from typing import Any

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

from ..models.order import OrderStatus 



class OrderItemBase(BaseModel):
    product_id: int
    product_name: str 
    price: float = Field(ge=0)
    quantity: int = Field(ge=1)
    result_price: float

class OrderItemCreate(OrderItemBase):
    ...

class OrderItemRead(OrderItemBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class OrderBase(BaseModel):
    user_id: int
    status: OrderStatus = OrderStatus.CREATED

    total_quantity: int = Field(ge=0)
    total_price: float = Field(ge=0)


class OrderCreate(OrderBase):
    items: list[OrderItemCreate]

class OrderRead(OrderBase):
    id: int
    items: list[OrderItemRead] = []

    created_at: datetime

    external_id: str|None = None
    payment_details: dict[str, Any] | None = None
    paid_at: datetime |None = None
    
    model_config = ConfigDict(from_attributes=True)

class OrderWithPaymentResponce(BaseModel):
    order: OrderRead
    payment_url: str

class OrderUpdate(BaseModel):
    status: OrderStatus | None = None 
    external_id: str|None = None
    payment_details: dict[str, Any] | None = None

    paid_at: datetime |None = None


