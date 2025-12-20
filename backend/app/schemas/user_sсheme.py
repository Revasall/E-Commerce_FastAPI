from pydantic import BaseModel, ConfigDict, EmailStr, Field
from ..models.user import UserRole


class UserBase(BaseModel):
    
    username: str = Field(max_length=30)
    email: EmailStr

    first_name: str = Field(max_length=30)
    last_name: str = Field(max_length=30)
    image: str | None = Field(default=None)



class UserCreate(UserBase):
    password: str = Field(max_length=30)

class UserRead(UserBase):
    
    id: int
    role: UserRole 

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    
    username: str | None = Field(default=None, max_length=20)
    email: EmailStr | None = None
    password: str | None = Field(default=None, max_length=20)
    
    first_name: str | None = Field(default=None, max_length=30)
    last_name: str | None = Field(default=None, max_length=30)
    image: str | None = Field(default=None)