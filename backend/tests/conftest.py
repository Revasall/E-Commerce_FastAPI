import pytest_asyncio, pytest
from datetime import datetime, timedelta
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from ..app.main import app
from ..app.models.user import User, UserRole
from ..app.models import Base, Category, Product
from ..app.database.database import get_session


SQLALCHEMY_DATABASE_URL = 'sqlite+aiosqlite:///:memory:?cache=shared'

engine_test = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True)
TestingSessionLocal = async_sessionmaker(engine_test, expire_on_commit=False)

@pytest_asyncio.fixture(scope='session', autouse=True)
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine_test.dispose()

@pytest_asyncio.fixture
async def session():
    async with TestingSessionLocal() as session:
        yield session

@pytest_asyncio.fixture
async def client(session):
    async def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as ac:
        yield ac
    app.dependency_overrides.clear()

@pytest_asyncio.fixture(scope='function')
async def test_user(session):
    """Create one test user for all tests"""

    user = User(
        username = 'John123',
        email = 'john_doe@test.com',
        #password = '123'
        hashed_password = '$argon2id$v=19$m=65536,t=3,p=4$Bh852Wf9IrbTXKc9Ygxeaw$2dOzYG8rzUHHjI2teX8h3GhP4O8Sl0LUb+P0999Ph3U',
        role = UserRole.USER,

        first_name = 'John',
        last_name = 'Doe',
        image = 'images/1'
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    yield user

    #Delete user from database
    await session.delete(user)
    await session.commit()

@pytest_asyncio.fixture(scope='function')
async def test_category(session):
    """Create one test category for all tests"""

    category = Category(
        title = 'documents',
        slug = 'documents'
    )

    session.add(category)
    await session.commit()
    await session.refresh(category)
    yield category

    await session.delete(category)
    await session.commit()

@pytest_asyncio.fixture(scope='function')
async def test_product(session):
    """Create one test product for all tests"""

    product = Product(
        title = 'Essay',
        description = 'An essay of up to five pages with an analis a specific topic',
        price = 150.00,

        category_id = 1,

        image = 'images/documents/essay1'
    )

    session.add(product)
    await session.commit()
    await session.refresh(product)
    yield product

    await session.delete(product)
    await session.commit()


