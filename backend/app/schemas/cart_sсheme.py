from pydantic import BaseModel, ConfigDict, Field


class CartItemBase(BaseModel):
    cart_id: int
    product_id: int
    quantity: int 
    image_url: str | None = Field(default=None)


class CartItemCreate(CartItemBase):
    ...

class CartItemRead(CartItemBase):
    product_title: str
    price: float
    total_price: float

    model_config = ConfigDict(from_attributes=True)


# class CartItemUpdate(Base):
#     ...

class Cart(BaseModel):
    user_id: int
    items: list[CartItemRead]
    total_quantity: int
    total_price: float
