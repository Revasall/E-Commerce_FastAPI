from pydantic import BaseModel, ConfigDict, EmailStr, Field
from ..models.user import UserRole


class UserBase(BaseModel):
    """
    Base attributes for a user identity.
    Used as a foundation for registration and profile viewing.
    """
    username: str = Field(..., max_length=30, description="Unique display name")
    email: EmailStr = Field(..., description="Valid email address for communications and login")

    first_name: str = Field(..., max_length=30, description="User's legal first name")
    last_name: str = Field(..., max_length=30, description="User's legal last name")
    image: str | None = Field(default=None, description="URL to the user's profile picture")
    role: UserRole = Field(default=UserRole.USER, description="System access level (user/admin)")



class UserCreate(UserBase):
    """
    Schema for new user registration. 
    Includes sensitive password data which is never returned in responses.
    """
    
    hashed_password: str = Field(..., min_length=8, max_length=30, description="Raw password string for registration")

class UserRead(UserBase):
    """
    User profile representation for API responses.
    Excludes sensitive security credentials.
    """

    id: int = Field(..., description="Internal database unique identifier")

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    """
    Schema for partial profile updates. 
    All fields are optional to allow flexible user edits.
    """
    
    username: str | None = Field(default=None, max_length=20)
    email: EmailStr | None = None
    password: str | None = Field(default=None, max_length=20)
    
    first_name: str | None = Field(default=None, max_length=30)
    last_name: str | None = Field(default=None, max_length=30)
    image: str | None = Field(default=None)