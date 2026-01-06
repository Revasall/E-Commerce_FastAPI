from fastapi import Depends
from typing import Annotated, List
from sqlalchemy.ext.asyncio import AsyncSession


from ..repository.user_repository import UserRepository
from ..schemas.user_sсheme import UserBase, UserCreate, UserRead, UserUpdate
from ..models.user import User
from ..core.exceptions import ObjectNotFoundError, ObjectAlreadyExistsError
from ..core.utils import ensure_exists
from ..database.database import SessionDep

class UserService:
    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)

    async def create_user(self, user_data: UserCreate) -> User:
        existing = await self.repository.get_user_by_username(user_data.username)
        if existing:
            raise ObjectAlreadyExistsError('User with this username already exist.')
        existing = await self.repository.get_user_by_email(user_data.email)
        if existing:
            raise ObjectAlreadyExistsError('User with this email already exist.')
        
        hashed_password = user_data.password
        new_user = await self.repository.create_user(user_data)

        return new_user
    
    async def get_all_users(self) -> List[UserRead]:
        users = await self.repository.get_all_users()

        return ensure_exists(
            obj=users,
            entity_name='User',
            exception=ObjectNotFoundError,
            validate_scheme=UserRead
        )
    
    async def get_user_by_id(self, 
                             user_id: int, 
                             scheme: bool
                             ) -> UserRead | User:
        user = await self.repository.get_user_by_id(user_id)

        return ensure_exists(
            obj=user,
            entity_name='User',
            exception=ObjectNotFoundError,
            validate_scheme= UserRead if scheme else None
        )
    
    
    async def get_user_by_username(self, 
                                   username: str,
                                   scheme: bool
                                   ) -> UserRead | User:
        user = await self.repository.get_user_by_username(username)
        
        return ensure_exists(
            obj=user,
            entity_name='User',
            exception=ObjectNotFoundError,
            validate_scheme= UserRead if scheme else None
        )
    
    async def get_user_by_email(self, 
                                email: str,
                                scheme: bool
                                ) -> UserRead | User:
        
        user = await self.repository.get_user_by_email(email)
        
        return ensure_exists(
            obj=user,
            entity_name='User',
            exception=ObjectNotFoundError,
            validate_scheme= UserRead if scheme else None
        )
    
    async def update_user(self, user_id: int, user_data: UserUpdate) -> UserRead:
        
        if user_data.username:
            existing = await self.repository.get_user_by_username(user_data.username)
            if existing:
                raise ObjectAlreadyExistsError('User with this username already exist.')
            
        if user_data.email:
            existing = await self.repository.get_user_by_email(user_data.email)
            if existing:
                raise ObjectAlreadyExistsError('User with this email already exist.')
            
        user = await self.repository.update_user(user_id=user_id, user_data=user_data)

        return UserRead.model_validate(user)
    
    async def delete_user(self, user_id: int) -> UserRead:
        user = await self.repository.delete_user(user_id)

        return ensure_exists(
            obj=user,
            entity_name='User',
            exception=ObjectNotFoundError,
            validate_scheme=UserRead
        )
    
def get_user_service(session: SessionDep) -> UserService:
    return UserService(session)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]