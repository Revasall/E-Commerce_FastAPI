import jwt
from pwdlib import PasswordHash
from datetime import timedelta, datetime, timezone

from ..config.config import settings
from ..models.user import User
from .exceptions import InvalidTokenError, InvalidTokenTypeError, ExpiredTokenError


class SecurityService:
    """
    Handles authentication security including password hashing and JWT management.
    
    This service abstracts the complexity of cryptographic operations, 
    providing a high-level API for token lifecycle and credential verification.
    """

    def __init__(self):
        self.SECRET_KEY = settings.security.SECRET_KEY
        self.ALGORITHM = settings.security.ALGORITHM
        self.ACCESS_TOKEN_EXPIRE_MINUTES = settings.security.ACCESS_TOKEN_EXPIRE_MINUTES
        self.REFRESH_TOKEN_EXPIRE_DAYS = settings.security.REFRESH_TOKEN_EXPIRE_DAYS
        self.password_hash = PasswordHash.recommended()
        
    def get_password_hash(self, password: str) -> str:
        """Generates a secure salted hash from a plain-text password."""
        return self.password_hash.hash(password)
    
    def verify_password(
            self,
            plain_passwrod: str,
            hashed_passwrod: str
            ) -> bool:
        """Verifies a plain password against its hashed version."""
        return self.password_hash.verify(plain_passwrod, hashed_passwrod)


    def create_jwt(
            self,
            payload: dict, 
            expires_delta: timedelta
            ) -> str:
        
        """Low-level helper to encode a JWT with a specific expiration."""
        
        to_encode = payload.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({'exp': expire})
        encode_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

        return encode_jwt

    def create_access_token(
            self,
            user: User,
            expires_delta: int | None = None
            ) -> str:
        """Generates a short-lived access token for user authentication."""
        
        payload = {
            'sub': str(user.id),
            'username': user.username,
            'role': user.role.value,
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
        """Generates a long-lived refresh token used to obtain new access tokens."""

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
        """Decodes and validates a JWT token.

        Checks signature validity, expiration, and enforces token type 
        to prevent 'token substitution' attacks (e.g., using refresh as access).

        Args:
            token: The raw JWT string.
            expected_type: Either 'access' or 'refresh'.

        Raises:
            InvalidTokenTypeError: If token_type claim doesn't match expected_type.
            ExpiredTokenError: If the 'exp' claim is in the past.
            InvalidTokenError: For any other decoding issues (signature, etc).
        """
    
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            
            # Critical: prevent using a long-lived Refresh token as an Access token
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