from pydantic import BaseModel, Field, ConfigDict


class ProductBase(BaseModel):
    title: str = Field(max_length=50)
    category_id: int
    price: float = Field(gt=0)
    description: str | None = Field(default=None, max_length=1000)
    image: str

class ProductCreate(ProductBase):
    ...

class ProductRead(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class ProductUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=50)
    category_id: int | None = None
    price: float | None = None
    description: str | None = Field(default=None, max_length=1000)
    image: str | None = None
