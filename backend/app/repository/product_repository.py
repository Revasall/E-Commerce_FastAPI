from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from ..models.product import Product 
from ..schemas.product_sсheme import ProductCreate, ProductUpdate
from ..core.exceptions import ObjectAlreadyExistsError

class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, product_data: ProductCreate) -> Product | None: 
        try:
            new_product = Product(**product_data.model_dump())
            self.db.add(new_product)
            await self.db.commit()
            await self.db.refresh(new_product)
            return new_product
        except IntegrityError:
            await self.db.rollback()
            raise ObjectAlreadyExistsError('Product with this title already exist.')
        
    async def get_all(self) -> List[Product] | None:
        result = await self.db.execute(select(Product))
        return list(result.scalars().all())
    
    async def get_by_category(self, category_id: int) -> List[Product] | None:
        result = await self.db.execute(select(Product).where(Product.category_id == category_id))
        return list(result.scalars().all())
    
    async def get_by_id(self, product_id: int) -> Product | None:
        result = await self.db.scalar(select(Product).where(Product.id == product_id))
        return result
    
    async def get_by_title(self, title: str) -> Product | None:
        result = await self.db.scalar(select(Product).where(Product.title == title))
        return result
    
    async def update(self, product_id: int, product_data: ProductUpdate) -> Product | None:
        product = await self.db.scalar(select(Product).where(Product.id == product_id))
        if product:   
            for key, value in product_data.model_dump(exclude_unset=True).items():
                if value:
                    setattr(product, key, value)
            await self.db.commit()
            await self.db.refresh(product)
        return product
        
    async def delete(self, product_id: int) -> Product | None:
        product = await self.db.scalar(select(Product).where(Product.id == product_id))

        if product:
            await self.db.delete(product)
            await self.db.commit()
            return product
        
        return None