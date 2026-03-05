# from pydantic import BaseModel, Field

# class Token(BaseModel):
#     """
#     Standard OAuth2 token response.
#     Contains both short-lived access and long-lived refresh tokens.
#     """

#     status: str = Field(..., description="JWT access token for resource authorization")
#     message: str = Field(..., description="JWT refresh token to obtain new access tokens")
