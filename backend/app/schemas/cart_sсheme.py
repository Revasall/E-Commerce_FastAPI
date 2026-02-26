from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class CartItemBase(BaseModel):
    cart_id: int
    product_id: int
    quantity: int = Field(gt=0)
    image_url: str | None = Field(default=None)


class CartItemCreate(CartItemBase):
    ...

class CartItemRead(BaseModel):
    id: int
    
    cart_id: int
    product_id: int
    quantity: int = Field(gt=0)
    image_url: str | None = Field(default=None)

    product_title: str
    price: float
    total_price: float

    model_config = ConfigDict(from_attributes=True)


class CartItemUpdate(BaseModel):
    quantity: int = Field(gt=0)

class CartScheme(BaseModel):
    id: int

    user_id: int
    items: list[CartItemRead]
    total_quantity: int
    total_price: float
