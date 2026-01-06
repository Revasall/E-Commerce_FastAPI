from typing import List
from fastapi import APIRouter, status

from ..schemas.user_sсheme import UserRead, UserCreate, UserUpdate
from ..services.user_service import UserServiceDep
from ..api.deps import UserDep


router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/', response_model=List[UserRead])
async def get_all_users(
    service: UserServiceDep
):
    
    return await service.get_all_users()

@router.get('/{user_id}', response_model=UserRead)
async def get_user_by_id(
    user_id: int,
    service: UserServiceDep
):
    return await service.get_user_by_id(user_id)

@router.get('/me', response_model=UserRead)
async def get_current_user(
    current_user: UserDep
    ):

    return current_user

@router.put('/me', response_model=UserRead)
async def update_user(
    current_user: UserDep,
    user_data: UserUpdate,
    service: UserServiceDep):

    return await service.update_user(current_user.id, user_data)

@router.delete('/me', response_model=UserRead)
async def delete_user(
    current_user: UserDep,
    service: UserServiceDep
    ):

    return await service.delete_user(current_user.id)
