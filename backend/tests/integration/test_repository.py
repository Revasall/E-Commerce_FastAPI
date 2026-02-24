import pytest

from backend.app.repository.category_repository import CategoryRepository
from backend.app.schemas.category_sсheme import CategoryCreate, CategoryUpdate
from backend.app.models.category import Category

from backend.app.repository.product_repository import ProductRepository
from backend.app.schemas.product_sсheme import ProductCreate, ProductUpdate
from backend.app.models.product import Product

from backend.app.models.cart import Cart, CartItem 
from backend.app.repository.cart_repository import CartRepository
from backend.app.schemas.cart_sсheme import CartItemCreate

from backend.app.repository.order_repository import OrderRepository
from backend.app.schemas.order_sсheme import OrderCreate, OrderItemCreate, OrderUpdate
from backend.app.models.order import Order, OrderItem, OrderStatus

from ...app.repository.user_repository import UserRepository
from ...app.models.user import User
from ...app.schemas.user_sсheme import UserCreate, UserRole, UserUpdate
from ...app.core.exceptions import ObjectAlreadyExistsError


@pytest.mark.asyncio
class TestUserRepository:

    async def test_create_and_del_user(self, session):
        user_rep = UserRepository(db=session)
        
        user = UserCreate(
            username='test_us',
            email='test@test.com',
            first_name='Test',
            last_name='TestTest',
            hashed_password='123321'
        )

        
        admin_user = user.model_copy()
        admin_user.username = 'test_us_2'
        admin_user.email = 'admin@test.com'
        admin_user.role = UserRole.ADMIN

        good_res = await user_rep.create_user(user)
        assert isinstance(good_res, User) and good_res.username == user.username
        assert good_res.role == UserRole.USER

        with pytest.raises(ObjectAlreadyExistsError) as err:
            await user_rep.create_user(user)
        assert err.value.status_code == 409

        admin_res = await user_rep.create_user(admin_user)
        assert admin_res.role == UserRole.ADMIN

        good_del = await user_rep.delete_user(admin_res.id)
        assert good_del.username == admin_res.username

        bad_del = await user_rep.delete_user(99)
        assert bad_del is None 

    async def test_get_all_users(self, session):
        user_rep = UserRepository(db=session)

        result = await user_rep.get_all_users()

        assert isinstance(result, list)
        assert isinstance(result[0], User)

    async def test_get_user_by_data(self, session, test_user):
        user_rep = UserRepository(db=session)

        res_good_username = await user_rep.get_user_by_username('John123')
        res_bad_username = await user_rep.get_user_by_username('bad_us')
        assert res_good_username.username == 'John123'
        assert res_bad_username is None

        res_good_id = await user_rep.get_user_by_id(test_user.id)
        res_bad_id = await user_rep.get_user_by_id(100)
        assert res_good_id.id == test_user.id
        assert res_bad_id is None

        res_good_email = await user_rep.get_user_by_email('john_doe@test.com')
        res_bad_email = await user_rep.get_user_by_email('test.test@test.test')
        assert res_good_email.email == 'john_doe@test.com'
        assert res_bad_email is None

    async def test_update_user(self, session, test_user):
        user_rep = UserRepository(session)

        update_data = UserUpdate(
            username='Update_John'
        )
        update_user = await user_rep.update_user(test_user.id, update_data)
        bad_upd = await user_rep.update_user(99, update_data)

        assert update_user.username == update_data.username
        assert bad_upd is None










@pytest.mark.asyncio
class TestProductRepository:

    async def test_create_and_del_product(self, session):
        product_rep = ProductRepository(db=session)
        
        good_product = ProductCreate(
            title = 'test_product',
            price = 1.0,
            category_id= 1,
            description='test_des'
        )


        good_res = await product_rep.create(good_product)
        assert good_res.title == good_product.title
        good_res_id = good_res.id

        with pytest.raises(ObjectAlreadyExistsError) as err:
            await product_rep.create(good_product)

        assert err.value.status_code == 409

        good_del = await product_rep.delete(good_res_id)
        bad_del = await product_rep.delete(99)

        assert good_del.title == good_res.title
        assert bad_del is None 

    async def test_get_all_products(self, session, test_product):
        product_rep = ProductRepository(db=session)

        result = await product_rep.get_all()

        assert isinstance(result, list)
        assert isinstance(result[0], Product)

    async def test_get_product_by_data(self, session, test_product):
        product_rep = ProductRepository(db=session)

        res_good_title = await product_rep.get_by_title('Essay')
        res_bad_title = await product_rep.get_by_title('bad_prod')
        assert res_good_title.title == 'Essay'
        assert res_bad_title is None

        res_good_id = await product_rep.get_by_id(test_product.id)
        res_bad_id = await product_rep.get_by_id(100)
        assert res_good_id.id == test_product.id
        assert res_bad_id is None

        res_good_category = await product_rep.get_by_category(test_product.category_id)
        res_bad_category = await product_rep.get_by_category(100)
        assert isinstance(res_good_category, list) and res_good_category[0].category_id == test_product.category_id
        assert res_bad_category == []

    async def test_update_product(self, session, test_product):
        product_rep = ProductRepository(db=session)

        update_data = ProductUpdate(
            title='Update_Product'
        )
        update_product = await product_rep.update(test_product.id, update_data)
        bad_upd = await product_rep.update(99, update_data)

        assert update_product.title == update_data.title
        assert bad_upd is None






@pytest.mark.asyncio
class TestCategoryRepository:

    async def test_create_and_del_category(self, session):
        category_rep = CategoryRepository(db=session)
        
        good_category = CategoryCreate(
            title='test_category',
            slug='test_slug'
        )

        good_res = await category_rep.create(good_category)
        good_res_id = good_res.id
        assert good_res.title == good_category.title

        with pytest.raises(ObjectAlreadyExistsError) as err:
            await category_rep.create(good_category)

        assert err.value.status_code == 409

        good_del = await category_rep.delete(good_res_id)
        bad_del = await category_rep.delete(99)

        assert good_del.title == good_res.title
        assert bad_del is None 

    async def test_get_all_category(self, session, test_category):
        category_rep = CategoryRepository(db=session)

        result = await category_rep.get_all()

        assert isinstance(result, list)
        assert isinstance(result[0], Category)

    async def test_get_category_by_data(self, session, test_category):
        category_rep = CategoryRepository(db=session)

        res_good_title = await category_rep.get_by_title('documents')
        res_bad_title = await category_rep.get_by_title('bad_cat')
        assert res_good_title.title == 'documents'
        assert res_bad_title is None

        res_good_id = await category_rep.get_by_id(test_category.id)
        res_bad_id = await category_rep.get_by_id(100)
        assert res_good_id.id == test_category.id
        assert res_bad_id is None

        res_good_slug = await category_rep.get_by_slug('documents')
        res_bad_slug = await category_rep.get_by_slug('bad_slug')
        assert res_good_slug.slug == 'documents'
        assert res_bad_slug is None

    async def test_update_category(self, session, test_category):
        category_rep = CategoryRepository(db=session)

        update_data = CategoryUpdate(
            title='Update_category'
        )
        update_product = await category_rep.update(test_category.id, update_data)
        bad_upd = await category_rep.update(99, update_data)

        assert update_product.title == update_data.title
        assert bad_upd is None



@pytest.mark.asyncio
class TestCartRepository:

    async def test_create_and_get_cart(self, session, test_user):
        repo = CartRepository(db=session)
        
        # 1. Checking the creation of the cart
        new_cart = await repo.create_cart(user_id=test_user.id)
        assert isinstance(new_cart, Cart)
        assert new_cart.user_id == test_user.id

        # 2. Checking the receipt of a cart by user_id
        found_cart = await repo.get_cart_by_user_id(test_user.id)
        assert found_cart.id == new_cart.id

    async def test_add_and_get_item(self, session, test_cart, test_product):
        repo = CartRepository(db=session)
        
        item_data = CartItemCreate(
            cart_id=test_cart.id,
            product_id=test_product.id,
            quantity=2,
            image_url="test_url"
        )

        # 1. Adding item
        item = await repo.add_item(item_data)
        assert item.product_id == test_product.id
        assert item.quantity == 2

        # Getting a item from the cart (by cart_id and product_id)
        found_item = await repo.get_item(test_cart.id, test_product.id)
        assert found_item.id == item.id

        # 3. Getting a item by ID
        found_by_id = await repo.get_item_by_id(item.id)
        assert found_by_id.id == item.id

    async def test_update_item_quantity(self, session, test_cart, test_product):
        repo = CartRepository(db=session)
        
        # Adding item 
        item_data = CartItemCreate(cart_id=test_cart.id, product_id=test_product.id, quantity=1)
        item = await repo.add_item(item_data)

        # Updating quantity
        updated_item = await repo.update_item_quantity(item.id, quantity=5)
        assert updated_item.quantity == 5

        # Check for a non-existent ID
        bad_update = await repo.update_item_quantity(999, quantity=10)
        assert bad_update is None

    async def test_remove_item(self, session, test_cart, test_product):
        repo = CartRepository(db=session)
        
        item_data = CartItemCreate(cart_id=test_cart.id, product_id=test_product.id, quantity=1)
        item = await repo.add_item(item_data)

        # Remove exisitng item
        delete_res = await repo.remove_item(item.id)
        assert delete_res is True

        # Checking that the item is no longer available
        check_item = await repo.get_item_by_id(item.id)
        assert check_item is None

        # Removing a non-existent product
        bad_delete = await repo.remove_item(999)
        assert bad_delete is False

    async def test_clear_cart_and_get_items(self, session, test_cart, test_product):
        repo = CartRepository(db=session)
        
        # Adding item in cart
        item_data = CartItemCreate(cart_id=test_cart.id, product_id=test_product.id, quantity=1)
        await repo.add_item(item_data)

        # 1. Check that the list of all items in the shopping cart has been received
        items = await repo.get_cart_items(test_cart.id)
        assert len(items) == 1
        assert isinstance(items[0], CartItem)

        # 2. Clear cart
        clear_res = await repo.clear_cart(test_cart.id)
        assert clear_res is True

        # Check that there are no items left
        items_after = await repo.get_cart_items(test_cart.id)
        assert len(items_after) == 0


@pytest.mark.asyncio
class TestOrderRepository:

    async def test_create_order(self, session, test_user, test_product):
        repo = OrderRepository(db=session)
        
        order_item = OrderItemCreate(
            product_id=test_product.id,
            product_name=test_product.title,
            price=test_product.price,
            quantity=2,
            result_price=test_product.price * 2
        )
        
        order_data = OrderCreate(
            user_id=test_user.id,
            total_quantity=2,
            total_price=test_product.price * 2,
            items=[order_item]
        )

        order = await repo.create_order(order_data)
        order_items = await repo.get_order_items(order.id)
        
        assert order.id is not None
        assert order.user_id == test_user.id
        assert len(order_items) == 1
        assert order_items[0].product_name == test_product.title


    async def test_get_orders_by_user_id(self, session, test_user, test_order):
        repo = OrderRepository(db=session)
        
        orders = await repo.get_all_orders_by_user_id(test_user.id)
        
        assert isinstance(orders, list)
        assert len(orders) >= 1
        assert orders[0].user_id == test_user.id

    async def test_get_item_by_id(self, session, test_order, test_product):
        repo = OrderRepository(db=session)
        
        items = await repo.get_order_items(test_order.id)
        item = await repo.get_item_by_id(items[0].id)
        assert item.id == items[0].id

        not_found = await repo.get_item_by_id(999)
        assert not_found is None

    async def test_get_order_by_id(self, session, test_user, test_order):
        repo = OrderRepository(db=session)

        order = await repo.get_order_by_id(test_order.id)
        assert order.id == test_order.id
        
        not_found = await repo.get_order_by_id(999)
        assert not_found is None

    async def test_update_order_full(self, session, test_order):
        repo = OrderRepository(db=session)
        
        update_info = OrderUpdate(
            status=OrderStatus.PAID,
            external_id="PAY-12345",
            payment_details={"method": "card"},
            paid_at="2023-01-01T00:00:00"  # Пример даты
        )
        updated_order = await repo.update_order(test_order.id, update_info)
        
        assert updated_order.status == OrderStatus.PAID
        assert updated_order.external_id == "PAY-12345"
        assert updated_order.payment_details == {"method": "card"}

        bad_update = await repo.update_order(999, update_info)
        assert bad_update is None

    async def test_get_item(self, session, test_user, test_order, test_product):
        repo = OrderRepository(db=session)
        
        item = await repo.get_item(test_order.id, test_product.id)
        assert item is not None
        assert item.product_name == test_product.title