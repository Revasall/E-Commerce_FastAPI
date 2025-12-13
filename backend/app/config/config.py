from pydantic_settings import BaseSettings
from pydantic import ConfigDict, Field
from typing import List


class AppSettings(BaseSettings):
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
    model_config = ConfigDict(env_file = '.env', extra='ignore')

    SECRET_KEY: str = Field(default='secretkey')
    ALGORITHM: str = Field(default='HS256')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=30)

class DataBaseSettings(BaseSettings):
    model_config = ConfigDict(env_file = '.env', extra='ignore')

    DB_USER: str = Field(default='postgres')
    DB_PASSWORD: str = Field(default='password')
    DB_HOST: str = Field(default='localhost')
    DB_PORT: str = Field(default='5432')
    DB_NAME: str = Field(default='e-commerce_api')
    DB_ECHO: bool = Field(default=True)
    @property
    def database_url(self) -> str:
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


class Settings:
    def __init__(self):
        self.app = AppSettings()
        self.security = SecuritySettings()
        self.database = DataBaseSettings()


settings = Settings()




