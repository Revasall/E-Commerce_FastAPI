import jwt
from typing import Annotated
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, HTTPBearer

from ..models.user import User, UserRole
from ..schemas.user_sсheme import UserRead
from ..database.database import SessionDep
from ..services.auth_service import AuthService, AuthServiceDep
from ..services.user_service import UserService, get_user_service
from ..services.product_service import ProductService, get_product_service
from ..services.category_service import CategoryService, get_category_service


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')
http_bearer = HTTPBearer()

def get_user_service(session: SessionDep) -> UserService:
    return UserService(session)

def get_auth_service(session: SessionDep) -> AuthService:
    return AuthService(session)

def get_product_service(session: SessionDep) -> ProductService:
    return ProductService(session)

def get_category_service(session: SessionDep) -> CategoryService:
    return CategoryService(session)

async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        service: AuthServiceDep
        ) -> UserRead:
    
    return await service.get_current_user(token)


UserDep = Annotated[UserRead, Depends(get_current_user)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]
CategoryServiceDep = Annotated[CategoryService, Depends(get_category_service)]

class RoleCheck:
    def __init__(self, allowed_roles: list[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: UserDep):
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='You do not have sufficient rights to perform this operation.'
            )
        return user
    
allow_admin = RoleCheck([UserRole.ADMIN])
     
