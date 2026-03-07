from typing import List
from fastapi import APIRouter, Request, status

from ..schemas.user_sсheme import UserRead, UserUpdate
from ..services.user_service import UserServiceDep
from ..api.deps import UserDep
from ..core.limiter import limiter


router = APIRouter(prefix='/users', tags=['Users'])


@router.get(
        '/', 
        response_model=List[UserRead],
        summary="Get all users"
        )
@limiter.limit('10/minute')
async def get_all_users(
    request: Request,
    service: UserServiceDep
    ):
    """
    Retrieve a list of all registered users. 
    Typically restricted to administrators in a production environment.
    """
    
    return await service.get_all_users()

@router.get(
        '/me', 
        response_model=UserRead,
        summary="Get current user profile"
        )
@limiter.limit('10/minute')
async def get_current_user(
    request: Request,
    current_user: UserDep):
    """Return the profile data of the currently authenticated user based on the JWT token."""
    
    return current_user

@router.get(
        '/{user_id}', 
        response_model=UserRead,
        summary="Get user by ID"
        )
@limiter.limit('10/minute')
async def get_user_by_id(
    request: Request,
    user_id: int,
    service: UserServiceDep
):
    """Fetch public profile information for a specific user by their unique ID."""

    return await service.get_user_by_id(user_id, True)

@router.put(
        '/me', 
        response_model=UserRead,
        summary="Update current user profile"
        )
@limiter.limit('10/minute')
async def update_user(
    request: Request,
    current_user: UserDep,
    user_data: UserUpdate,
    service: UserServiceDep):
    """Update personal information for the currently logged-in user."""

    return await service.update_user(current_user.id, user_data)

@router.delete(
        '/me', 
        response_model=UserRead, 
        status_code=status.HTTP_200_OK,
        summary="Delete current user account")
@limiter.limit('5/minute')
async def delete_user(
    request: Request,
    current_user: UserDep,
    service: UserServiceDep
    ):
    """Permanently remove the currently authenticated user's account from the system."""
    
    return await service.delete_user(current_user.id)
