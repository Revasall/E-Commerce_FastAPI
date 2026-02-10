from pydantic import BaseModel, ConfigDict, Field

class CategoryBase(BaseModel):
    title: str = Field(max_length=30)
    slug: str|None = Field(max_length=50, default=None)


class CategoryCreate(CategoryBase):
    ...

class CategoryRead(CategoryBase):
    id: int


    model_config = ConfigDict(from_attributes=True)

class CategoryUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=30)
    slug: str | None = Field(default=None, max_length=30)



