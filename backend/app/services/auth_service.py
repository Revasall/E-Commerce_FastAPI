import jwt
from fastapi import Depends
from typing import Annotated, List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer


from ..services.user_service import UserService
from ..schemas.user_sсheme import UserCreate, UserRead, UserUpdate
from ..schemas.token_sсheme import Token
from ..models.user import User
from ..core.exceptions import ObjectNotFoundError, InvalidCredentialsError, InvalidTokenError, UserCreateError
from ..core.utils import ensure_exists
from ..core.security import security_service
from ..database.database import SessionDep

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')
http_bearer = HTTPBearer()

class AuthService:
    def __init__(self, db: AsyncSession):
        self.service = UserService(db)
        self.security = security_service

    async def get_current_user(
            self,
            token: str
            ) -> UserRead:
        
        try: 
            payload = self.security.decode_jwt_token(token, expected_type='access')
            user_id: str = payload.get('sub')
            if user_id is None:
                raise InvalidTokenError
            user = await self.service.get_user_by_id(int(user_id), scheme=True)
            return user
        except jwt.PyJWTError:
            raise InvalidTokenError
        except ObjectNotFoundError:
            raise InvalidCredentialsError

             

    
    async def autenticate_user(
            self, 
            email:str,
            plain_password: str
            ) -> User:
        try:
            user = await self.service.get_user_by_email(email, False)
        except ObjectNotFoundError:
            raise InvalidCredentialsError
        if not self.security.verify_password(plain_password, user.hashed_password):
            raise InvalidCredentialsError
        return user
    
    async def login_for_token(
            self,
            email: str,
            password: str
            ) -> Token:
        
        user =  await self.autenticate_user(email, password)
        if not user:
            raise InvalidCredentialsError()
        access_token = self.security.create_access_token(user)
        refresh_token = self.security.create_refresh_token(user)

        return Token(
            access_token=access_token,
            refresh_token=refresh_token
            )
        
    async def register_user(
            self, 
            user_reg_data: UserCreate
            ) -> Token: 
        
        hashed_password = self.security.get_password_hash(user_reg_data.hashed_password)
        user_reg_data.hashed_password = hashed_password
        new_user = await self.service.create_user(user_reg_data)

        if not new_user:
            raise UserCreateError()
        
        access_token = self.security.create_access_token(new_user)
        refresh_token = self.security.create_refresh_token(new_user)

        return Token(
            access_token=access_token,
            refresh_token=refresh_token
        ) 

    async def refresh_access_token(
            self,
            refresh_token: str
            ) -> Token:
        
        payload = self.security.decode_jwt_token(refresh_token, 'refresh')
        user_id = int(payload['sub'])
        if user_id is None:
            raise InvalidTokenError()
        
        user = await self.service.get_user_by_id(user_id, False)
        new_access_token = self.security.create_access_token(user)
        new_refresh_token = self.security.create_refresh_token(user)

        return Token(
            access_token=new_access_token,
            refresh_token=new_refresh_token
        )
    

def get_auth_service(session: SessionDep) -> AuthService:
    return AuthService(session)

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
        
        




