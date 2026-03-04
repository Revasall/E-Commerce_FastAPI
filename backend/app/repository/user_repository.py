from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from ..models.user import User
from ..schemas.user_sсheme import UserCreate, UserUpdate
from ..core.exceptions import ObjectAlreadyExistsError

class UserRepository:
    """
    Data access layer for User entities.
    Handles user persistence, profile retrieval, and integrity checks for unique fields.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user_data: UserCreate) -> User | None: 
        """
        Registers a new user record.
        Raises ObjectAlreadyExistsError if the username or email is already taken.
        """

        try:
            new_user = User(**user_data.model_dump(exclude='password'))
            new_user.hashed_password = user_data.password
            self.db.add(new_user)
            await self.db.commit()
            await self.db.refresh(new_user)
            return new_user
        except IntegrityError:
            await self.db.rollback()
            raise ObjectAlreadyExistsError('User with this username or email')
        
    async def get_all_users(self) -> List[User] | None:
        """Retrieves a list of all registered users."""

        result = await self.db.execute(select(User))
        return list(result.scalars().all())
    
    async def get_user_by_username(self, username: str) -> User | None:
        """Finds a user by their unique username."""

        result = await self.db.scalar(select(User).where(User.username == username))
        return result
    
    async def get_user_by_id(self, user_id: int) -> User | None:
        """Fetches a single user by primary key ID."""

        result = await self.db.scalar(select(User).where(User.id == user_id))
        return result
    
    async def get_user_by_email(self, email: str) -> User | None:
        """Finds a user by their unique email address."""

        result = await self.db.scalar(select(User).where(User.email == email))
        return result
    
    async def update_user(self, user_id: int, user_data: UserUpdate) -> User | None:
        """
        Updates user profile information.
        """

        user = await self.db.scalar(select(User).where(User.id == user_id))
        if user:
            for key, value in user_data.model_dump(exclude_unset=True).items():
                if value:
                    if key == 'password':
                        user.hashed_password == user_data.password
                    setattr(user, key, value)
            await self.db.commit()
            await self.db.refresh(user)
        return user
        
    async def delete_user(self, user_id: int) -> User | None:
        """
        Removes a user record from the system.
        Returns the deleted User instance or None if not found.
        """

        user = await self.db.get(User, user_id)#await self.db.scalar(select(User).where(User.id == user_id))

        if user:
            await self.db.delete(user)
            await self.db.commit()
            return user
        
        return None