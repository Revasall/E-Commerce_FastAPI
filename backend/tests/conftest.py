import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from backend.app.models.order import Order, OrderItem


from ..app.main import app
from ..app.models.user import User, UserRole
from ..app.models.cart import Cart, CartItem 
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
    existing_user = await session.get(User, user.id)
    if existing_user:
        try:
            await session.delete(user)
            await session.commit()
        except:
            await session.rollback()

@pytest_asyncio.fixture(scope='function')
async def test_admin(session):
    """Create one test user for all tests"""

    user = User(
        username = 'admin_John123',
        email = 'admin@test.com',
        #password = '123'
        hashed_password = '$argon2id$v=19$m=65536,t=3,p=4$Bh852Wf9IrbTXKc9Ygxeaw$2dOzYG8rzUHHjI2teX8h3GhP4O8Sl0LUb+P0999Ph3U',
        role = UserRole.ADMIN,

        first_name = 'John',
        last_name = 'Doe',
        image = 'images/1'
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    yield user

    #Delete user from database
    existing_user = await session.get(User, user.id)
    if existing_user:
        try:
            await session.delete(user)
            await session.commit()
        except:
            await session.rollback()


@pytest_asyncio.fixture(scope='function')
async def test_refresh_token(client, test_user):
    """Returns authorization headers with a valid access token."""
    responce = await client.post('/auth/login', data={
        'username': test_user.email,
        'password': '123'
    })
    data = responce.json()
    refresh_token = data['refresh_token']
    yield refresh_token


@pytest_asyncio.fixture(scope='function')
async def test_auth_header(client, test_user):
    """Returns authorization headers with a valid access token."""
    responce = await client.post('/auth/login', data={
        'username': test_user.email,
        'password': '123'
    })
    data = responce.json()
    token = data.get('access_token')
    yield ({'Authorization': f'Bearer {token}'} if token else {})

@pytest_asyncio.fixture(scope='function')
async def test_admin_auth_header(client, test_admin):
    """Returns authorization headers with a valid access token."""
    responce = await client.post('/auth/login', data={
        'username': test_admin.email,
        'password': '123'
    })
    data = responce.json()
    token = data.get('access_token')
    yield ({'Authorization': f'Bearer {token}'} if token else {})



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

    existing_category = await session.get(Category, category.id)
    if existing_category:
        try:
            await session.delete(category)
            await session.commit()
        except:
            await session.rollback()


@pytest_asyncio.fixture(scope='function')
async def test_product(session, test_category):
    """Create one test product for all tests"""

    product = Product(
        title = 'Essay',
        description = 'An essay of up to five pages with an analis a specific topic',
        price = 150.00,

        category_id = test_category.id,

        image = 'images/documents/essay1'
    )

    session.add(product)
    await session.commit()
    await session.refresh(product)
    yield product

    existing_product = await session.get(Product, product.id)
    if existing_product:
        try:
            await session.delete(product)
            await session.commit()
        except:
            await session.rollback()



@pytest_asyncio.fixture(scope='function')
async def test_cart(session, test_user):
    """Create one test cart for all tests"""
    cart = Cart(user_id=test_user.id)
    session.add(cart)
    await session.commit()
    await session.refresh(cart)
    yield cart

    existing_cart = await session.get(Cart, cart.id)
    if existing_cart:
        try:
            await session.delete(existing_cart)
            await session.commit()
        except:
            await session.rollback()

@pytest_asyncio.fixture(scope='function')
async def test_cart_item(session, test_cart,test_product):
    """Create one test item for cart"""
    item= CartItem(
            cart_id=test_cart.id,
            product_id=test_product.id,
            quantity=2,
            image_url="test_url"
        )
    
    session.add(item)
    await session.commit()
    await session.refresh(item)
    yield item

    existing_cart_item = await session.get(CartItem, item.id)
    if existing_cart_item:
        try:
            await session.delete(existing_cart_item)
            await session.commit()
        except:
            await session.rollback()


@pytest_asyncio.fixture(scope='function')
async def test_order(session, test_user, test_product, test_cart, test_cart_item):
    """Create test order and test item"""
        
    order = Order(
        user_id = test_cart.user_id,
        total_quantity=test_cart_item.quantity,
        total_price=test_cart_item.price*test_cart_item.quantity,
        )
    session.add(order)
    await session.flush()

    items = [
        OrderItem(
            order_id = order.id,
            product_id=test_cart_item.product_id,
            product_name=test_cart_item.product_title,
            price=test_cart_item.price,
            quantity=test_cart_item.quantity,
            result_price=test_cart_item.price*test_cart_item.quantity
        )]



    
    session.add_all(items)
    await session.commit()
    await session.refresh(order)
    
    yield order

    existing_order = await session.get(Order, order.id)
    if existing_order:
        try:
            await session.delete(order)
            await session.commit()
        except:
            await session.rollback()

