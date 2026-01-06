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
    def __init__(self, db:AsyncSession):
        self.repository = CategoryRepository(db)


    async def create(self, category_data: CategoryCreate) -> CategoryRead:
        # Availability check and automatic slug generation
        if not category_data.slug:
            category_data.slug = slugify(category_data.title)

        existing = await self.repository.get_by_slug(category_data.slug)
        if existing:
            raise ObjectAlreadyExistsError('Category with this slug already exists.')
        
        new_category = await self.repository.create(category_data)

        return CategoryRead.model_validate(new_category)

    async def get_all(self) -> List[CategoryRead]:
        categories = await self.repository.get_all()
        
        return ensure_exists(
            obj=categories,
            entity_name='Category',
            exception=ObjectNotFoundError,
            validate_scheme=CategoryRead)
    
    async def get_by_id(self, category_id: int) -> CategoryRead: 
        category = await self.repository.get_by_id(category_id)

        return ensure_exists(
            obj=category,
            entity_name='Category',
            exception=ObjectNotFoundError,
            validate_scheme=CategoryRead)
    
    async def get_by_title(self, title: str) -> CategoryRead:
        category = await self.repository.get_by_title(title)

        return ensure_exists(
            obj=category,
            entity_name='Category',
            exception=ObjectNotFoundError,
            validate_scheme=CategoryRead)
    
    
    async def get_by_slug(self, slug: str) -> CategoryRead:

        category = await self.repository.get_by_slug(slug)

        return ensure_exists(
            obj=category,
            entity_name='Category',
            exception=ObjectNotFoundError,
            validate_scheme=CategoryRead)
    
    
    async def update(self, category_id: int, category_data: CategoryUpdate) -> CategoryRead:

        if category_data.slug:
            existing = await self.repository.get_by_slug(category_data.slug)
            if existing:
                raise ObjectAlreadyExistsError('Category with this slug already exists.')

        category = await self.repository.update(category_id = category_id, category_data = category_data)
        
        return CategoryRead.model_validate(category)
        

    async def delete(self, category_id: int) -> None:
        category = await self.repository.delete(category_id=category_id)

        return ensure_exists(category, 'Category', ObjectNotFoundError, CategoryRead)


def get_category_service(session: SessionDep) -> CategoryService:
    return CategoryService(session)

CategoryServiceDep = Annotated[CategoryService, Depends(get_category_service)]

 