from fastapi import Depends
from slugify import slugify
from typing import Annotated, List
from sqlalchemy.ext.asyncio import AsyncSession


from ..repository.category_repository import CategoryRepository
from ..schemas.category_sсheme import CategoryCreate, CategoryRead, CategoryUpdate
from ..core.exceptions import ObjectNotFoundError, ObjectAlreadyExistsError
from ..core.utils import ensure_exists
from ..database.database import SessionDep


class CategoryService:
    """
    Business logic layer for managing product categories.
    Handles slug generation, uniqueness validation, and object existence checks.
    """

    def __init__(self, db:AsyncSession):
        self.repository = CategoryRepository(db)


    async def create(self, category_data: CategoryCreate) -> CategoryRead:
        """
        Creates a new category with automatic slug generation.
        
        Logic:
        1. If slug is not provided, generates it from the title.
        2. Checks if a category with this slug already exists to prevent URL collisions.
        """

        if not category_data.slug:
            category_data.slug = slugify(category_data.title)

        existing = await self.repository.get_by_slug(category_data.slug)
        if existing:
            raise ObjectAlreadyExistsError('Category with this slug already exists.')
        
        new_category = await self.repository.create(category_data)

        return CategoryRead.model_validate(new_category)

    async def get_all(self) -> List[CategoryRead]:
        """Retrieves all categories, validated against the CategoryRead schema."""

        categories = await self.repository.get_all()
        
        return ensure_exists(
            obj=categories,
            entity_name='Category',
            exception=ObjectNotFoundError,
            validate_scheme=CategoryRead)
    
    async def get_by_id(self, category_id: int) -> CategoryRead:
        """Fetches a category by ID and ensures it exists."""

        category = await self.repository.get_by_id(category_id)

        return ensure_exists(
            obj=category,
            entity_name='Category',
            exception=ObjectNotFoundError,
            validate_scheme=CategoryRead)
    
    async def get_by_title(self, title: str) -> CategoryRead:
        """Retrieves a category by its title for frontend routing."""

        category = await self.repository.get_by_title(title)

        return ensure_exists(
            obj=category,
            entity_name='Category',
            exception=ObjectNotFoundError,
            validate_scheme=CategoryRead)
    
    
    async def get_by_slug(self, slug: str) -> CategoryRead:
        """Retrieves a category by its URL slug for frontend routing."""

        category = await self.repository.get_by_slug(slug)

        return ensure_exists(
            obj=category,
            entity_name='Category',
            exception=ObjectNotFoundError,
            validate_scheme=CategoryRead)
    
    
    async def update(self, category_id: int, category_data: CategoryUpdate) -> CategoryRead:
        """
        Updates category details. 
        If the title changes without a new slug, re-generates the slug.
        """

        if not category_data.slug:
            category_data.slug = slugify(category_data.title)

        existing = await self.repository.get_by_slug(category_data.slug)
        if existing and existing.id != category_id:
            raise ObjectAlreadyExistsError('Category with this slug already exists.')

        category = await self.repository.update(category_id = category_id, category_data = category_data)
        
        return ensure_exists(
            obj=category,
            entity_name='Category',
            exception=ObjectNotFoundError,
            validate_scheme=CategoryRead
            )     

    async def delete(self, category_id: int) -> None:
        """Removes a category and returns its final state before deletion."""

        category = await self.repository.delete(category_id=category_id)
        return ensure_exists(
            category, 
            'Category', 
            ObjectNotFoundError, 
            CategoryRead)


def get_category_service(session: SessionDep) -> CategoryService:
    return CategoryService(session)

CategoryServiceDep = Annotated[CategoryService, Depends(get_category_service)]

 