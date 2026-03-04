"""
Application configuration classes.

Each class inherits from `pydantic_settings.BaseSettings` and
loads values ​​from the environment/.env.
A `settings` instance is created upon import and is then
used throughout the project.
"""

from pydantic_settings import BaseSettings
from pydantic import ConfigDict, Field, field_validator
from typing import List


class AppSettings(BaseSettings):
    "Basic application settings (name, debug, CORS, static paths)."""

    model_config = ConfigDict(env_file = '.env', extra='ignore')
    
    APP_NAME: str = Field(default="FastAPI Shop")
    DEBUG: bool = Field(default=True)
    CORS_ORIGINS: List[str] | str = Field(default=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ])
    STATIC_DIR: str = Field(default="static")
    IMAGES_DIR: str = Field(default="static/images")


class SecuritySettings(BaseSettings):
    """JWT Encryption Parameters and Token Timeouts"""

    model_config = ConfigDict(env_file = '.env', extra='ignore')

    SECRET_KEY: str = Field(default='secretkey')
    ALGORITHM: str = Field(default='HS256')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=30)

class DataBaseSettings(BaseSettings):
    """Database connection settings"""

    model_config = ConfigDict(env_file = '.env', extra='ignore')

    POSTGRES_USER: str = Field(default='postgres')
    POSTGRES_PASSWORD: str = Field(default='password')
    POSTGRES_HOST: str = Field(default='localhost')
    POSTGRES_PORT: str = Field(default='5432')
    POSTGRES_NAME: str = Field(default='e-commerce_fastapi')
    ECHO: bool = Field(default=True)
    @property
    def database_url(self) -> str:
        return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_NAME}'

class ECommerceSettings(BaseSettings):
    """""
    Payment gateway / e‑commerce specific settings.

    Used for Yookassa integration: account id, secret key, return URL
    and currency.  The validator restricts the currency to supported
    values.
    """
    model_config = ConfigDict(env_file = '.env', extra='ignore')

    ACCOUNT_ID: str = Field(default='1')
    SECRET_KEY: str = Field(default='test_')
    RETURN_URL: str = Field(default="http://localhost:3000/order-success")
    PAYMENT_CURRENCY: str = Field(default='USD')

    @field_validator("PAYMENT_CURRENCY")
    def validate_currency(cls, v):
        allowed = ["BYN", "USD", "EUR", "RUB"]
        if v.upper() not in allowed:
            raise ValueError(f"Currency {v} is not supported")
        return v.upper()
    
class Settings:
    """A collection of all your settings: app, security, database, ecommerce."""
    def __init__(self):
        
        self.app = AppSettings()
        self.security = SecuritySettings()
        self.database = DataBaseSettings()
        self.ecommerce = ECommerceSettings()


settings = Settings()




