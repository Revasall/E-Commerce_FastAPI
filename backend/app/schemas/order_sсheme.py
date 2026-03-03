
from typing import Any

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

from ..models.order import OrderStatus 



class OrderItemBase(BaseModel):
    """
    Base attributes for an item within an order.
    Captures a snapshot of the product state at the moment of purchase.
    """

    product_id: int = Field(..., description="ID of the purchased product")
    product_name: str = Field(..., description="Name of the product at checkout time")
    price: float = Field(ge=0, description="Unit price at the time of order")
    quantity: int = Field(ge=1, description="Number of units purchased")
    result_price: float = Field(..., description="Total price for this line item (price * quantity)")

class OrderItemCreate(OrderItemBase):
    """Schema for internal order item initialization."""
    ...

class OrderItemRead(OrderItemBase):
    """Schema for displaying order item details in history."""
    
    id: int
    model_config = ConfigDict(from_attributes=True)


class OrderBase(BaseModel):
    """
    Core order attributes including status and calculated totals.
    """

    user_id: int = Field(..., description="Owner of the order")
    status: OrderStatus = Field(default=OrderStatus.CREATED, description="Current lifecycle state of the order")
    total_quantity: int = Field(ge=0, description="Total count of all items")
    total_price: float = Field(ge=0, description="Final amount to be paid")


class OrderCreate(OrderBase):
    """Schema for creating a new order record from cart data."""
    items: list[OrderItemCreate]

class OrderRead(OrderBase):
    """
    Comprehensive order data including payment metadata and item breakdown.
    """

    id: int
    items: list[OrderItemRead] = Field(default_factory=list)
    created_at: datetime = Field(..., description="Timestamp when the order was placed")
    
    # Payment gateway integration fields
    external_id: str | None = Field(None, description="Transaction ID from the payment provider (e.g., Yookassa)")
    payment_details: dict[str, Any] | None = Field(None, description="Raw payment provider response for debugging")
    paid_at: datetime | None = Field(None, description="Timestamp of successful payment confirmation")
    
    model_config = ConfigDict(from_attributes=True)

class OrderWithPaymentResponce(BaseModel):
    """
    Wrapper for initial order placement response.
    Combines order details with the URL for the user to complete payment.
    """

    order: OrderRead
    payment_url: str = Field(..., description="External link to the payment gateway checkout page")

class OrderUpdate(BaseModel):
    """Schema for partial order updates. All fields are optional."""
    
    status: OrderStatus | None = None 
    external_id: str|None = None
    payment_details: dict[str, Any] | None = None

    paid_at: datetime |None = None


