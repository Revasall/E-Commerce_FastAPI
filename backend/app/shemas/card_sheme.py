from pydantic import BaseModel, ConfigDict, Field


class CartItemBase(BaseModel):
    product_id: int
    quantity: int 

class CartItemCreate(CartItemBase):
    ...

class CartItemGet(CartItemBase):
    product_title: str
    price: float
    total_price: float
    image_urd: str | None = Field(default=None)

    model_config = ConfigDict(from_attributes=True)


class CartItemUpdate(CartItemBase):
    ...

class Cart(BaseModel):
    user_id: int
    items: list[CartItemGet]
    total_quantity: int
    total_price: float