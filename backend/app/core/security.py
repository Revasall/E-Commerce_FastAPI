import jwt
from pwdlib import PasswordHash
from datetime import timedelta, datetime, timezone

from ..config.config import SecuritySettings
from ..models.user import User
from .exceptions import InvalidTokenError, InvalidTokenTypeError, ExpiredTokenError, InvalidCredentialsError


class SecurityService:

    def __init__(self):
        self.SECRET_KEY = SecuritySettings.SECRET_KEY
        self.ALGORTITHM = SecuritySettings.ALGORITHM
        self.ACCESS_TOKEN_EXPIRE_MINUTES = SecuritySettings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.REFRESH_TOKEN_EXPIRE_DAYS = SecuritySettings.REFRESH_TOKEN_EXPIRE_DAYS
        self.password_hash = PasswordHash.recommended()
        
    def get_password_hash(self, password: str) -> str:
        return self.password_hash.hash(password)
    
    def verify_password(
            self,
            plain_passwrod: str,
            hashed_passwrod: str
            ) -> bool:
        return self.password_hash.verify(plain_passwrod, hashed_passwrod)


    def create_jwt(
            self,
            payload: dict, 
            expires_delta: timedelta
            ) -> str:
        to_encode = payload.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({'exp': expire})
        encode_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORTITHM)

        return encode_jwt

    def create_access_token(
            self,
            user: User,
            expires_delta: int | None = None
            ) -> str:
        
        payload = {
            'sub': str(user.id),
            'email': user.username,
            'role': user.role,
            'token_type': 'access'
        }
        if not expires_delta:
            expires_delta = self.ACCESS_TOKEN_EXPIRE_MINUTES

        expires_delta = timedelta(minutes=expires_delta)

        return self.create_jwt(payload, expires_delta)

    def create_refresh_token(
            self,
            user: User,
            expires_delta: int | None = None
            ) -> str:
        
        payload = {
            'sub': str(user.id),
            'token_type': 'refresh'
        }
        if not expires_delta:
            expires_delta = self.REFRESH_TOKEN_EXPIRE_DAYS
        expires_delta = timedelta(days=expires_delta)

        return self.create_jwt(payload, expires_delta)

    def decode_jwt_token(
            self,
            token: str,
            expected_type: str
            ) -> dict:
    
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORTITHM])
            if payload['token_type'] != expected_type:
                raise InvalidTokenTypeError(
                    token_type=payload['token_type'],
                    expected_type=expected_type
                )
            return payload
        except jwt.ExpiredSignatureError:
            raise ExpiredTokenError()
        except jwt.InvalidTokenError:
            raise InvalidTokenError()
    
security_service = SecurityService()