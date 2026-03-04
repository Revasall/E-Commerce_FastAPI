from typing import Annotated
from fastapi import APIRouter, status, Depends, Request
from fastapi.security import HTTPBearer, OAuth2PasswordRequestForm, HTTPAuthorizationCredentials

from ..schemas.user_sсheme import UserCreate
from ..schemas.token_sсheme import Token
from ..services.auth_service import AuthServiceDep


router = APIRouter(prefix='/auth', tags=['Auth'])
http_bearer = HTTPBearer()

@router.post('/register', 
             response_model=Token, 
             status_code=status.HTTP_201_CREATED,
             summary="Register a new user",
             responses={400: {"description": "User already exists or validation failed"}}
             )
async def registration_user(
    reques: Request,
    user_reg_data: UserCreate,
    service: AuthServiceDep
    ) -> Token:
    """
    Creates a new user profile and returns an initial set of JWT tokens.
    """

    return await service.register_user(user_reg_data)

@router.post(
        '/login',
        response_model=Token,
        summary="Authenticate user and get tokens",
        responses={401: {"description": "Invalid username or password"}}
        )
async def login(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: AuthServiceDep
    ) -> Token:
    """
    Standard OAuth2 compatible login. 
    Accepts 'username' and 'password' to issue access/refresh tokens.
    """
    
    return await service.login_for_token(form_data.username, form_data.password)

@router.post(
        '/refresh',
        response_model=Token,
        summary="Refresh access token",
        responses={401: {"description": "Invalid or expired refresh token"}}
        )
async def refresh_access_token(
    request: Request,
    service: AuthServiceDep,
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
    ) -> Token:
    """
    Exchanges a Refresh token for a new Access token. 
    Requires a valid Refresh token in the Authorization header.
    """

    return await service.refresh_access_token(credentials.credentials)