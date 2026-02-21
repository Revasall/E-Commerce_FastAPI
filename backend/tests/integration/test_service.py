import pytest

from backend.app.models.user import User
from backend.app.schemas.cart_sсheme import CartItemCreate, CartItemUpdate, CartScheme
from backend.app.schemas.category_sсheme import CategoryCreate, CategoryRead, CategoryUpdate
from backend.app.schemas.product_sсheme import ProductCreate, ProductRead, ProductUpdate
from backend.app.schemas.user_sсheme import UserCreate, UserRead, UserUpdate
from backend.app.services.cart_service import CartService
from backend.app.services.product_service import ProductService
from backend.app.services.user_service import UserService
from backend.app.services.auth_service import AuthService
from backend.app.services.category_service import CategoryService
from backend.app.core.exceptions import InvalidCredentialsError, ObjectAlreadyExistsError, ObjectNotFoundError, InvalidTokenError


@pytest.mark.asyncio
class TestUserService:
    async def test_create_and_delete_user(self, session):
        user_ser = UserService(session)
        
        user = UserCreate(
            username='TestCreate',
            email='create@test.com',
            first_name='Test',
            last_name='Test',
            hashed_password='123321'
        )

        user_in_db = await user_ser.create_user(user)

        assert user_in_db.username == user.username
        
        with pytest.raises(ObjectAlreadyExistsError) as err_username:
            bad_user = user.model_copy()
            bad_user.email = 'new@test.com'
            await user_ser.create_user(bad_user)

        assert err_username.value.status_code == 409 and err_username.value.args[0] == 'User with this username already exist.'

        with pytest.raises(ObjectAlreadyExistsError) as err_mail:
            bad_user = user.model_copy()
            bad_user.username = 'BadTestUsername'
            await user_ser.create_user(bad_user)

        assert err_mail.value.status_code == 409 and err_mail.value.args[0] == 'User with this email already exist.'

        del_user = await user_ser.delete_user(user_in_db.id)
        assert del_user.id == user_in_db.id

        with pytest.raises(ObjectNotFoundError) as err_del:
            await user_ser.delete_user(user_in_db.id)
        
        assert err_del.value.status_code == 404

    async def test_get_user_by_data(self, session, test_user):
        
        user_ser = UserService(session)

        all_us = await user_ser.get_all_users()
        assert isinstance(all_us, list) and isinstance(all_us[0], UserRead)

        user_id = await user_ser.get_user_by_id(all_us[0].id, True)
        assert user_id.id == all_us[0].id and isinstance(user_id, UserRead)
        with pytest.raises(ObjectNotFoundError) as err_id:
            await user_ser.get_user_by_id(99, True)
        assert err_id.value.status_code == 404

        user_username = await user_ser.get_user_by_username('John123', False)
        assert user_username.username == 'John123' and isinstance(user_username, User)
        with pytest.raises(ObjectNotFoundError) as err_username:
            await user_ser.get_user_by_username('BadTest', False)
        assert err_username.value.status_code == 404

        user_email = await user_ser.get_user_by_email('john_doe@test.com', False)
        assert user_email.email == 'john_doe@test.com' and isinstance(user_email, User)
        with pytest.raises(ObjectNotFoundError) as err_email:
            await user_ser.get_user_by_email('bad_email@test.com', False)
        assert err_email.value.status_code == 404

    async def test_update_user(self, session, test_user):

        user_ser = UserService(session)

        update_data = UserUpdate(
            username='Update_John_serv'
        )
        update_user = await user_ser.update_user(test_user.id, update_data)
        
        assert update_user.username == update_data.username




@pytest.mark.asyncio
class TestAuthService:
    
    async def test_register_user(self, session):

        auth_serv = AuthService(session)

        new_user = UserCreate(
            username='TestRegist',
            email='regist@test.com',
            first_name='Test',
            last_name='Test',
            hashed_password='123321'
        )

        token_data = await auth_serv.register_user(new_user)

        assert token_data.access_token is not None
        assert token_data.refresh_token is not None

        user_in_db = await auth_serv.service.get_user_by_username(new_user.username, scheme=False)
        assert auth_serv.security.verify_password('123321', user_in_db.hashed_password)

    async def test_autenticate_and_login(self,session,test_user):

        auth_serv = AuthService(session)

        password = '123'

        auth_user = await auth_serv.autenticate_user(test_user.email ,password)
        assert auth_user.email == test_user.email

        with pytest.raises(InvalidCredentialsError) as err_auth:
            await auth_serv.autenticate_user(test_user.email ,'bad_pass')
        assert err_auth.value.status_code == 401
        
        token_data = await auth_serv.login_for_token(test_user.email ,password)
        assert token_data.access_token is not None
        assert token_data.refresh_token is not None

        with pytest.raises(InvalidCredentialsError) as err_auth:
            await auth_serv.login_for_token(test_user.email ,'bad_pass')
        assert err_auth.value.status_code == 401

        
    async def test_get_current_user(self, session, test_user):

        auth_serv = AuthService(session)

        password = '123'
        token_data = await auth_serv.login_for_token(test_user.email ,password)

        good_user = await auth_serv.get_current_user(token_data.access_token)
        assert isinstance(good_user, UserRead)
        assert good_user.id == test_user.id and  good_user.email == test_user.email 

        with pytest.raises(InvalidTokenError) as err_token:
            await auth_serv.get_current_user('123')
        assert err_token.value.status_code == 401

    async def test_refresh_access_token(self, session, test_user):

        auth_serv = AuthService(session)

        password = '123'
        old_tokens = await auth_serv.login_for_token(test_user.email ,password)

        token_data = await auth_serv.refresh_access_token(old_tokens.refresh_token)
        assert token_data.access_token is not None
        assert  token_data.refresh_token is not None

        with pytest.raises(InvalidTokenError) as err_token:
            await auth_serv.refresh_access_token('123')
        assert err_token.value.status_code == 401


@pytest.mark.asyncio
class TestCategoryService:

    async def test_create_and_delete_category(self, session):

        category_ser = CategoryService(session)

        category_with_slug = CategoryCreate(
            title = 'test',
            slug = 'test'
            )
        
        category_without_slug = CategoryCreate(
            title = 'test2'
        )
        
        slug_category = await category_ser.create(category_with_slug)
        assert slug_category.title == category_with_slug.title

        no_slug_category = await category_ser.create(category_without_slug)
        assert no_slug_category.title == category_without_slug.title and no_slug_category.slug == 'test2'

        with pytest.raises(ObjectAlreadyExistsError) as err_create: 
            await category_ser.create(category_with_slug)
        assert err_create.value.status_code == 409


        delete_category = await category_ser.delete(slug_category.id)
        assert delete_category.id == slug_category.id

        with pytest.raises(ObjectNotFoundError) as err_delete:
            await category_ser.delete(99)
        assert err_delete.value.status_code == 404

    async def test_get_category(self, session, test_category):

        category_ser = CategoryService(session)

        all_category = await category_ser.get_all()
        assert isinstance(all_category, list) and isinstance(all_category[0], CategoryRead)

        id_category = await category_ser.get_by_id(test_category.id)
        assert id_category.id == test_category.id and isinstance(id_category, CategoryRead)
        with pytest.raises(ObjectNotFoundError) as err_id:
            await category_ser.get_by_id(99)
        assert err_id.value.status_code == 404

        title_category = await category_ser.get_by_title(test_category.title)
        assert title_category.title == test_category.title and isinstance(title_category, CategoryRead)
        with pytest.raises(ObjectNotFoundError) as err_title:
            await category_ser.get_by_title('no_title')
        assert err_title.value.status_code == 404

        slug_category = await category_ser.get_by_slug(test_category.slug)
        assert slug_category.slug == test_category.slug and isinstance(slug_category, CategoryRead)
        with pytest.raises(ObjectNotFoundError) as err_slug:
            await category_ser.get_by_slug('no_slug')
        assert err_slug.value.status_code == 404

    async def test_category_update(self, session, test_category):

        category_ser = CategoryService(session)

        category_update_data = CategoryUpdate(
            title = 'update_test',
            )

        update_category = await category_ser.update(test_category.id, category_update_data)
        assert update_category.id == test_category.id and update_category.title == category_update_data.title
        
        with pytest.raises(ObjectAlreadyExistsError) as err_slug_update:
            await category_ser.update(test_category.id-1, category_update_data)
        assert err_slug_update.value.status_code == 409

        with pytest.raises(ObjectNotFoundError) as err_id_update:
            await category_ser.update(99, CategoryCreate(title='bad_test'))
        assert err_id_update.value.status_code == 404




@pytest.mark.asyncio
class TestProductService:

    async def test_create_and_delete_product(self, session, test_category):

        product_ser = ProductService(session)

        product = ProductCreate(
            title='test_product',
            category_id=test_category.id,
            price=1.0,
            description='test',
            image='test'
        )

        good_product = await product_ser.create(product)
        assert isinstance(good_product, ProductRead) and good_product.title == product.title
        with pytest.raises(ObjectAlreadyExistsError) as err_create: 
            await product_ser.create(product)
        assert err_create.value.status_code == 409

        delete_product = await product_ser.delete_product(good_product.id)
        assert delete_product.id == good_product.id
        with pytest.raises(ObjectNotFoundError) as err_delete:
            await product_ser.delete_product(99)
        assert err_delete.value.status_code == 404
        

    async def test_get_product_by_data(self, session, test_product): 

        product_ser = ProductService(session)
        category_ser = CategoryService(session)

        all_products = await product_ser.get_all_products()
        assert isinstance(all_products, list) and isinstance(all_products[0], ProductRead) 

        category = await category_ser.get_by_id(test_product.category_id) 
        category_products = await product_ser.get_by_category(category.slug)
        assert isinstance(category_products, list) and category_products[0].category_id == test_product.category_id
        with pytest.raises(ObjectNotFoundError) as err_category:
            await product_ser.get_by_category(99)
        assert err_category.value.status_code == 404

        id_product = await product_ser.get_by_id(test_product.id)
        assert id_product.id == test_product.id
        with pytest.raises(ObjectNotFoundError) as err_id:
            await product_ser.get_by_id(99)
        assert err_id.value.status_code == 404

        title_product = await product_ser.get_by_title(test_product.title)
        assert title_product.title == test_product.title
        with pytest.raises(ObjectNotFoundError) as err_title:
            await product_ser.get_by_title('bad_title')
        assert err_title.value.status_code == 404

    async def test_update_product(self, session, test_product):

        product_ser = ProductService(session)

        update_data = ProductUpdate(
            title='update_product',
            price=10.0,
            description='update_test',
            )
        
        update_product = await product_ser.update_product(test_product.id, update_data)
        assert update_product.title == update_data.title and test_product.id == update_product.id 

        with pytest.raises(ObjectAlreadyExistsError) as err_title:
            await product_ser.update_product(test_product.id, update_data)
        assert err_title.value.status_code == 409

        with pytest.raises(ObjectNotFoundError) as err_id:
            await product_ser.update_product(99, ProductUpdate(title='new_title'))
        assert err_id.value.status_code == 404



@pytest.mark.asyncio
class TestCartService:

    async def test_create_cart(self, session, test_user):
        """Check: If the cart doesn't exist, the service creates it."""
        cart_serv = CartService(session)

        cart = await cart_serv.get_cart(test_user.id)
        assert isinstance(cart, CartScheme)
        assert cart.user_id == test_user.id
        assert isinstance(cart.items, list) and len(cart.items)==0
        assert cart.total_price == 0

    async def test_add_item_to_cart(self, session, test_user, test_product):
        """Check: if a new product has been added and recalculating the cart"""
        cart_serv = CartService(session)

        item_data = CartItemCreate(
            cart_id=0,
            product_id=test_product.id,
            quantity=2,
            image_url=test_product.image
        )

        cart_res = await cart_serv.add_item(test_user.id, item_data)
        assert len(cart_res.items) == 1
        assert cart_res.items[0].product_id == test_product.id
        assert cart_res.items[0].quantity == 2
        assert cart_res.total_quantity == 2
        assert cart_res.total_price == test_product.price * 2

        item_data.product_id= 999
        with pytest.raises(ObjectNotFoundError) as err_product:
            await cart_serv.add_item(test_user.id, item_data)
        assert err_product.value.status_code == 404

    async def test_add_item_increment_quantity(self, session, test_user, test_product):
        """Check: If the item is already in the cart, the quantity is increased."""        
        cart_ser = CartService(session)
        
        item_data = CartItemCreate(
            cart_id=0,
            product_id=test_product.id, 
            quantity=1, 
            )


        await cart_ser.add_item(test_user.id, item_data)

        cart_res = await cart_ser.add_item(test_user.id, item_data)
        assert len(cart_res.items) == 1
        assert cart_res.items[0].quantity == 2
        assert cart_res.total_quantity == 2

    async def test_update_item_quantity(self, session, test_user, test_product, test_cart):
        """Check: updating the quantity of an existing product"""
        cart_ser = CartService(session)
        
        item_data = CartItemCreate(product_id=test_product.id, 
                                   quantity=1, 
                                   cart_id=test_cart.id)
        
        initial_cart = await cart_ser.add_item(test_user.id, item_data)        

        update_data = CartItemUpdate(quantity=10)
        updated_cart = await cart_ser.update_item(test_user.id, initial_cart.id, update_data)
        assert updated_cart.items[0].quantity == 10
        assert updated_cart.total_price == test_product.price * 10

        with pytest.raises(ObjectNotFoundError) as err_item:
            await cart_ser.update_item(test_user.id, 999, update_data)
        assert err_item.value.status_code == 404

    async def test_remove_item(self, session, test_user, test_product, test_cart):
        """Checking if an item has been removed from the cart"""
        cart_ser = CartService(session)
        
        item_data = CartItemCreate(product_id=test_product.id, 
                                   quantity=1, 
                                   cart_id=test_cart.id)

        new_cart = await cart_ser.add_item(test_user.id, item_data)
        item = new_cart.items[0]

        cart_res = await cart_ser.remove_item(test_user.id, item.id)
        assert len(cart_res.items) == 0
        assert cart_res.total_price == 0

        with pytest.raises(ObjectNotFoundError) as err_item:
            await cart_ser.remove_item(test_user.id, 999)
        assert err_item.value.status_code == 404


    async def test_clear_cart(self, session, test_user, test_product, test_cart):
        """Checking clear cart"""
        cart_ser = CartService(session)
        
        item_data = CartItemCreate(product_id=test_product.id, 
                                   quantity=1, 
                                   cart_id=test_cart.id)
        
        await cart_ser.add_item(test_user.id, item_data)
        
        cart_res = await cart_ser.clear_cart(test_user.id)
        assert len(cart_res.items) == 0
        assert cart_res.total_quantity == 0

        with pytest.raises(ObjectNotFoundError) as err_clear:
            await cart_ser.clear_cart(test_user.id)
        assert err_clear.value.status_code == 404

