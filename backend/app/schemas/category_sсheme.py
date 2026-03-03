from pydantic import BaseModel, ConfigDict, Field

class CategoryBase(BaseModel):
    """
    Base attributes for a product category.
    """

    title: str = Field(..., max_length=30, description="Unique display name of the category")
    slug: str | None = Field(default=None, max_length=50, description="URL-friendly identifier (auto-generated if empty)")


class CategoryCreate(CategoryBase):
    """
    Schema for creating a new category.
    """
    ...

class CategoryRead(CategoryBase):
    """
    Schema for category output. Includes database-specific fields.
    """
    id: int = Field(..., description="Primary key ID")

    model_config = ConfigDict(from_attributes=True)

class CategoryUpdate(BaseModel):
    """
    Schema for partial category updates. All fields are optional.
    """
    title: str | None = Field(default=None, max_length=30)
    slug: str | None = Field(default=None, max_length=30)



