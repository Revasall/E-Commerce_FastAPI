import pytest

from backend.app.models.category import Category
from backend.app.models.product import Product
from backend.app.repository.category_repository import CategoryRepository
from backend.app.repository.product_repository import ProductRepository
from backend.app.schemas.category_sсheme import CategoryCreate, CategoryUpdate
from backend.app.schemas.product_sсheme import ProductCreate, ProductUpdate

from ...app.repository.user_repository import UserRepository
from ...app.models.user import User
from ...app.schemas.user_sсheme import UserCreate, UserRole, UserUpdate
from ...app.core.exceptions import ObjectAlreadyExistsError


@pytest.mark.asyncio
class TestUserRepository:

    async def test_create_and_del_user(self, session):
        user_rep = UserRepository(db=session)
        
        good_user = UserCreate(
            username='test_us',
            email='test@test.com',
            first_name='Test',
            last_name='TestTest',
            hashed_password='123321'
        )

        
        admin_user = good_user.model_copy()


        good_res = await user_rep.create_user(good_user)
        assert (good_res.username, good_res.email) == (good_user.username, good_user.email)
        assert good_res.id is not None

        with pytest.raises(ObjectAlreadyExistsError) as err:
            await user_rep.create_user(good_user)

        assert err.value.status_code == 409
        
        admin_user.username = 'test_us_2'
        admin_user.email = 'admin@test.com'
        admin_user.role = UserRole.ADMIN
        admin_res = await user_rep.create_user(admin_user)

        assert admin_res.role == admin_user.role

        good_del = await user_rep.delete_user(1)
        bad_del = await user_rep.delete_user(99)

        assert good_del.username == good_res.username
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

        res_good_id = await user_rep.get_user_by_id(2)
        res_bad_id = await user_rep.get_user_by_id(100)
        assert res_good_id.id == 2
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
        update_user = await user_rep.update_user(2, update_data)
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

        with pytest.raises(ObjectAlreadyExistsError) as err:
            await product_rep.create(good_product)

        assert err.value.status_code == 409

        good_del = await product_rep.delete(1)
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

        res_good_id = await product_rep.get_by_id(1)
        res_bad_id = await product_rep.get_by_id(100)
        assert res_good_id.id == 1
        assert res_bad_id is None

        res_good_category = await product_rep.get_by_category(1)
        res_bad_category = await product_rep.get_by_category(100)
        assert isinstance(res_good_category, list) and res_good_category[0].category_id == 1
        assert res_bad_category == []

    async def test_update_product(self, session, test_product):
        product_rep = ProductRepository(db=session)

        update_data = ProductUpdate(
            title='Update_Product'
        )
        update_product = await product_rep.update(1, update_data)
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
        assert good_res.title == good_category.title

        with pytest.raises(ObjectAlreadyExistsError) as err:
            await category_rep.create(good_category)

        assert err.value.status_code == 409

        good_del = await category_rep.delete(1)
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

        res_good_id = await category_rep.get_by_id(1)
        res_bad_id = await category_rep.get_by_id(100)
        assert res_good_id.id == 1
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
        update_product = await category_rep.update(1, update_data)
        bad_upd = await category_rep.update(99, update_data)

        assert update_product.title == update_data.title
        assert bad_upd is None


    

