from typing import Annotated
from fastapi import APIRouter, status, Depends, Request
from fastapi.security import HTTPBearer, OAuth2PasswordRequestForm, HTTPAuthorizationCredentials
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.user_sсheme import UserRead, UserCreate, UserUpdate
from ..schemas.token_sсheme import Token
from ..services.auth_service import AuthServiceDep


router = APIRouter(prefix='/auth', tags=['Auth'])
http_bearer = HTTPBearer()

@router.post('/register', response_model=Token, status_code=status.HTTP_201_CREATED)
async def registration_user(
    reques: Request,
    user_reg_data: UserCreate,
    service: AuthServiceDep
    ) -> Token:

    return await service.register_user(user_reg_data)

@router.post('/login')
async def login(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: AuthServiceDep
    ) -> Token:

    return await service.login_for_token(form_data.username, form_data.password)

@router.post('/refresh')
async def refresh_access_token(
    request: Request,
    service: AuthServiceDep,
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
    ) -> Token:

    return await service.refresh_access_token(credentials.credentials)