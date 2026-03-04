from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from ..core.exceptions import ObjectAlreadyExistsError
from ..schemas.category_sсheme import CategoryCreate, CategoryUpdate
from ..models.category import Category

class CategoryRepository:
    """
    Data access layer for product categories.
    Provides methods for CRUD operations and handles database integrity constraints.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, category_data: CategoryCreate) -> Category | None:
        """
        Creates a new category. 
        Raises ObjectAlreadyExistsError if a category with the same unique fields (slug/title) exists.
        """

        try:
            new_category = Category(**category_data.model_dump())
            self.db.add(new_category)
            await self.db.commit()
            await self.db.refresh(new_category)
            return new_category
        except IntegrityError:
            await self.db.rollback()
            raise ObjectAlreadyExistsError('Category with this slug already exist.')

    
    async def get_all(self) -> List[Category] | None:
        """Retrieves a list of all existing categories."""

        result = await self.db.execute(select(Category))
        return list(result.scalars().all())
    
    async def get_by_id(self, category_id: int) -> Category | None:
        """Fetches a single category by its primary key."""

        result = await self.db.scalar(select(Category).where(Category.id == category_id))
        return result
    
    async def get_by_title(self, title: str) -> Category | None:
        """Finds a category by its display title."""

        result = await self.db.scalar(select(Category).where(Category.title == title))
        return result
    
    async def get_by_slug(self, slug: str) -> Category | None:
        """Finds a category by its URL-friendly slug."""

        result = await self.db.scalar(select(Category).where(Category.slug == slug))
        return result
    
    async def update(self, category_id: int, category_data: CategoryUpdate) -> Category | None:
        """
        Updates category attributes. 
        Only non-None values from the update schema are applied.
        """

        category = await self.db.scalar(select(Category).where(Category.id == category_id))
        if category:    
            for key, value in category_data.model_dump(exclude_unset=True).items():
                if value:
                    setattr(category, key, value)
            await self.db.commit()
            await self.db.refresh(category)
        return category
    
    async def delete(self, category_id: int) -> Category | None:
        """
        Deletes a category from the database.
        Returns the deleted object or None if it is not found.
        When deleting a category, all products associated with it change their category ID to None.
        
        """
        
        category = await self.db.scalar(select(Category).where(Category.id == category_id))

        if category:
            await self.db.delete(category)
            await self.db.commit()
            return category

        return None