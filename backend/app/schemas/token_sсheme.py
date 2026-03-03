from pydantic import BaseModel, Field

class Token(BaseModel):
    """
    Standard OAuth2 token response.
    Contains both short-lived access and long-lived refresh tokens.
    """

    access_token: str = Field(..., description="JWT access token for resource authorization")
    refresh_token: str = Field(..., description="JWT refresh token to obtain new access tokens")
    token_type: str = Field(default='bearer', description="Type of the token, typically 'bearer'")

class TokenData(BaseModel):
    """
    Schema representing the payload extracted from a decoded JWT.
    """
    username: str | None = Field(default=None, description="Username (email) encoded in the 'sub' claim")