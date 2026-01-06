from fastapi import Depends, FastAPI
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from typing import AsyncGenerator, Annotated
from contextlib import asynccontextmanager

from ..models.base import Base
from ..config.config import settings

engine = create_async_engine(
    settings.database.database_url, 
    echo=settings.database.DB_ECHO
    )

async_session = async_sessionmaker(engine)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


SessionDep = Annotated[AsyncSession, Depends(get_session)]