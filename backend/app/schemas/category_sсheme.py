from pydantic import BaseModel, ConfigDict, Field

class CategoryBase(BaseModel):
    title: str = Field(max_length=30)

class CategoryCreate(CategoryBase):
    slug: str = Field(max_length=30)

class CategoryRead(CategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class CategoryUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=30)
    slug: str | None = Field(default=None, max_length=30)



