from pydantic import BaseModel, ConfigDict, Field

class CartItemBase(BaseModel):
    """Base schema for shopping cart items sharing common attributes."""

    cart_id: int = Field(..., description="ID of the parent cart")
    product_id: int = Field(..., description="Unique product identifier")
    quantity: int = Field(gt=0, description="Number of items, must be greater than zero")
    image_url: str | None = Field(default=None, description="URL of the product thumbnail")


class CartItemCreate(CartItemBase):
    """Schema for adding a new item to the cart."""
    ...

class CartItemRead(BaseModel):
    """
    Detailed schema for reading cart items. 
    Includes denormalized data like title and price for frontend efficiency.
    """

    id: int
    cart_id: int
    product_id: int
    quantity: int = Field(gt=0)
    image_url: str | None = Field(default=None)

    product_title: str = Field(..., description="Display name of the product")
    price: float = Field(..., description="Unit price at the time of retrieval")
    total_price: float = Field(..., description="Computed total (price * quantity)")

    model_config = ConfigDict(from_attributes=True)

class CartItemUpdate(BaseModel):
    """Schema for modifying existing cart item quantity."""

    quantity: int = Field(gt=0, description="New quantity for the item")

class CartScheme(BaseModel):
    """
    Complete shopping cart representation.
    Aggregation of items with calculated totals.
    """
    
    id: int = Field(..., description="Unique cart identifier")
    user_id: int = Field(..., description="Owner of the cart")
    items: list[CartItemRead] = Field(default_factory=list, description="List of products in the cart")
    total_quantity: int = Field(..., description="Total count of all items combined")
    total_price: float = Field(..., description="Grand total for the entire cart")

    model_config = ConfigDict(from_attributes=True)
