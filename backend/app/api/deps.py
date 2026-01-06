import jwt
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, HTTPBearer

import app.core.security as security
from ..models.user import User
from ..schemas.user_sсheme import UserRead
from ..database.database import SessionDep
from ..services.auth_service import AuthServiceDep
from ..services.user_service import UserService, get_user_service
from ..services.product_service import ProductService, get_product_service
from ..services.category_service import CategoryService, get_category_service


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')
http_bearer = HTTPBearer()

def get_user_service(session: SessionDep) -> UserService:
    return UserService(session)

def get_product_service(session: SessionDep) -> ProductService:
    return ProductService(session)

def get_category_service(session: SessionDep) -> CategoryService:
    return CategoryService(session)

async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        service: AuthServiceDep
        ) -> User:
    
    return await service.get_current_user(token)


UserDep = Annotated[User, Depends(get_current_user)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]
CategoryServiceDep = Annotated[CategoryService, Depends(get_category_service)]



     
