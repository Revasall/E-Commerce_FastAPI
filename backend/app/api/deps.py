
from typing import Annotated
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, HTTPBearer

from ..models.user import UserRole
from ..schemas.user_sсheme import UserRead
from ..services.auth_service import AuthServiceDep


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')
http_bearer = HTTPBearer()


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        service: AuthServiceDep
        ) -> UserRead:
    """Verifies the JWT token, returns the current user's profile."""
    
    return await service.get_current_user(token)


UserDep = Annotated[UserRead, Depends(get_current_user)]

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
     
