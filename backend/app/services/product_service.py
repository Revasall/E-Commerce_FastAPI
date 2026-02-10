from fastapi import Depends
from typing import Annotated, List
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.repository.category_repository import CategoryRepository


from ..repository.product_repository import ProductRepository
from ..schemas.product_sсheme import ProductCreate, ProductRead, ProductUpdate
from ..core.exceptions import ObjectNotFoundError, ObjectAlreadyExistsError
from ..core.utils import ensure_exists
from ..database.database import SessionDep

class ProductService:
    def __init__(self, db: AsyncSession):
        self.repository = ProductRepository(db)
        self.category_repository = CategoryRepository(db)

    async def create(self, product_data: ProductCreate) -> ProductRead:
        existing = await self.repository.get_by_title(product_data.title)
        if existing:
            raise ObjectAlreadyExistsError('Product with this title already exist.')
        
        new_product = await self.repository.create(product_data)

        return ensure_exists(
            obj=new_product,
            entity_name='Product',
            exception=ObjectNotFoundError,
            validate_scheme=ProductRead
        )
    
    async def get_all_products(self) -> List[ProductRead]:
        products = await self.repository.get_all()

        return ensure_exists(
            obj=products,
            entity_name='Product',
            exception=ObjectNotFoundError,
            validate_scheme=ProductRead
        )
    
    async def get_by_category(self, category_id: int) -> List[ProductRead]:
        is_category_exist = await self.category_repository.get_by_id(category_id)
        
        if is_category_exist:
            products = await self.repository.get_by_category(category_id)
            
            return ensure_exists(
                obj=products,
                entity_name='Product',
                exception=ObjectNotFoundError,
                validate_scheme=ProductRead
            )
        raise ObjectNotFoundError('Category')
        
    async def get_by_id(self, product_id: int) -> ProductRead:
        product = await self.repository.get_by_id(product_id)

        return ensure_exists(
            obj=product,
            entity_name='Product',
            exception=ObjectNotFoundError,
            validate_scheme=ProductRead
        )
    
    async def get_by_title(self, title: str) -> ProductRead:
        product = await self.repository.get_by_title(title)
        
        return ensure_exists(
            obj=product,
            entity_name='Product',
            exception=ObjectNotFoundError,
            validate_scheme=ProductRead
        )
    
    async def update_product(self,product_id: int, product_data: ProductUpdate) -> ProductRead:
        
        if product_data.title:
            existing = await self.repository.get_by_title(product_data.title)
            if existing:
                raise ObjectAlreadyExistsError('Product with this title already exist.')
            
        product = await self.repository.update(product_id=product_id, product_data=product_data)

        return ensure_exists(
            obj=product,
            entity_name='Product',
            exception=ObjectNotFoundError,
            validate_scheme=ProductRead
        )
    
    async def delete_product(self, product_id: int) -> ProductRead:
        product = await self.repository.delete(product_id)

        return ensure_exists(
            obj=product,
            entity_name='Product',
            exception=ObjectNotFoundError,
            validate_scheme=ProductRead
        )
    
def get_product_service(session: SessionDep) -> ProductService:
    return ProductService(session)

ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]