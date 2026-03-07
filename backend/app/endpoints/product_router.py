from typing import List
from fastapi import APIRouter, Request, status, Depends

from ..api.deps import UserDep, allow_admin

from ..schemas.product_sсheme import ProductRead, ProductCreate, ProductUpdate
from ..services.product_service import ProductServiceDep
from ..core.limiter import limiter


router = APIRouter(prefix='/products', tags=['Products'])

@router.post(
        '/', 
        response_model=ProductRead, 
        status_code=status.HTTP_201_CREATED, 
        dependencies=[Depends(allow_admin)],
        summary="Create product (Admin only)"
        )
async def create_product(
    current_user: UserDep,
    product_data: ProductCreate,
    service:ProductServiceDep
):
    """Adds a new product to the catalog."""
    
    return await service.create(product_data)

@router.get(
        '/', 
        response_model=List[ProductRead],
        summary="Get all products")
@limiter.limit('60/minute')
async def get_all_products(
    request: Request,
    service: ProductServiceDep):
    """Retrieves the full list of available products."""
    
    return await service.get_all_products()

@router.get(
        '/{category_slug}', 
        response_model=List[ProductRead],
        summary="Get products by category slug")
@limiter.limit('60/minute')
async def get_product_by_category(
    request: Request,
    category_slug: str,
    service: ProductServiceDep
    ):
    """Filters products by their category's URL-friendly slug."""

    return await service.get_by_category(category_slug)

@router.get(
        '/id/{product_id}', 
        response_model=ProductRead, 
        summary="Get product by ID"
        )
@limiter.limit('100/minute')
async def get_product_by_id(
    request: Request,
    product_id: int,
    service: ProductServiceDep
    ):
    """Fetches a specific product using its unique database ID."""
    
    return await service.get_by_id(product_id)

@router.put(
        '/{product_id}', 
        response_model=ProductRead, 
        dependencies=[Depends(allow_admin)],
        summary="Update product (Admin only)")
async def update_product(
    current_user: UserDep,
    product_id: int,
    product_data: ProductUpdate,
    service: ProductServiceDep):
    """Modifies existing product details."""

    return await service.update_product(product_id, product_data)

@router.delete(
        '/{product_id}', 
        response_model=ProductRead, 
        dependencies=[Depends(allow_admin)],
        summary="Delete product (Admin only)"
        )
async def delete_product(
    current_user: UserDep,
    product_id: int,
    service: ProductServiceDep
    ):
    """Removes a product from the database."""

    return await service.delete_product(product_id)
