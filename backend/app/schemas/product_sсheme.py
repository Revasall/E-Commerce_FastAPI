from pydantic import BaseModel, Field, ConfigDict


class ProductBase(BaseModel):
    """
    Base attributes for a product. 
    Defines common constraints for catalog items.
    """

    title: str = Field(..., max_length=50, description="Product name as displayed in the catalog")
    category_id: int | None = Field(default=None, description="ID of the category this product belongs to")
    price: float = Field(gt=0, description="Unit price, must be a positive number")
    description: str | None = Field(default=None, max_length=1000, description="Detailed product description")
    image: str | None = Field(default=None, max_length=1000, description="URL or path to the product image")

class ProductCreate(ProductBase):
    """Schema for adding a new product to the database."""
    ...

class ProductRead(ProductBase):
    """
    Schema for product output. 
    Includes database-generated fields.
    """

    id: int = Field(..., description="Unique product identifier")

    model_config = ConfigDict(from_attributes=True)

class ProductUpdate(BaseModel):
    """
    Schema for partial product updates. All fields are optional.
    """
    title: str | None = Field(default=None, max_length=50)
    category_id: int | None = None
    price: float | None = None
    description: str | None = Field(default=None, max_length=1000)
    image: str | None = None
