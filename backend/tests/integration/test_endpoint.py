import pytest

from backend.app.models.user import User
from backend.app.schemas.category_sсheme import CategoryRead


@pytest.mark.asyncio 
class TestAuthEndpoints:
    
    async def test_register_user(self, client):
        payload = {
            "username": "reg_test",
            "email": "reg@example.com",
            "first_name": "string",
            "last_name": "string",
            "image": "string",
            "role": "user",
            "hashed_password": "password"
            }

        responce = await client.post('/auth/register', json=payload)
        assert responce.status_code in (200, 201)
        data = responce.json()
        assert 'access_token' in data and 'refresh_token' in data and data['token_type'] == 'bearer'

        bad_resp = await client.post('/auth/register', json={})
        assert bad_resp.status_code == 422

    async def test_login(self, client, test_user):

        email = test_user.email
        password = '123'
        responce = await client.post(
            '/auth/login',
            data = {'username':email, 'password': password}
            )
        assert responce.status_code == 200
        data = responce.json()
        assert 'access_token' in data and 'refresh_token' in data

        bad_responce = await client.post(
            '/auth/login',
            data = {'username':'bad', 'password': 'bad'}
            )
        assert bad_responce.status_code == 401
        data = responce.json()


    async def test_refresh_token(self, client, test_refresh_token):

        #Using refresh for get new access and refresh tokens
        ref_responce = await client.post('/auth/refresh', headers={"Authorization": f"Bearer {test_refresh_token}"})
        assert ref_responce.status_code == 200
        ref_data = ref_responce.json()
        assert 'access_token' in ref_data and 'refresh_token' in ref_data






@pytest.mark.asyncio 
class TestUserEndpoints:

    async def test_get_current_user(self, client, test_user, test_auth_header):

        responce = await client.get('/users/me', headers=test_auth_header)
        assert responce.status_code == 200
        data = responce.json()
        assert data['username'] == test_user.username

        bad_responce = await client.get('/users/me', headers={'Authorization': f'Bearer 123'})
        assert bad_responce.status_code == 401

    async def test_get_user_by_id(self, client, test_user):

        responce = await client.get(f'/users/{test_user.id}')
        assert responce.status_code == 200
        data = responce.json()
        assert data['id'] == test_user.id

        bad_responce = await client.get(f'/users/99')
        assert bad_responce.status_code == 404
        
    async def test_update_user(self, client, test_user, test_auth_header):
        payload = {
            'username':'update_test_user',
            'email':'update_email@example.com',
            'password':'update_password'
        }

        responce = await client.put('/users/me', headers=test_auth_header, json = payload)
        assert responce.status_code == 200
        data = responce.json()
        assert data['username'] == payload['username'] and data['email'] == payload['email']


    async def test_delete_user(self, session, client, test_user, test_auth_header):

        responce = await client.delete('/users/me', headers = test_auth_header)
        data = responce.json()
        
        assert responce.status_code == 200
        assert int(data['id']) == test_user.id 
        assert data['email'] == test_user.email

        session.expire_all()
        user_in_db = await session.get(User, test_user.id)
        assert user_in_db is None






@pytest.mark.asyncio
class TestCategoryEndpoints:

    async def test_create_category(self, client, test_admin_auth_header, test_auth_header):
        
        payload = {
            "title":"test_endpoint",
            "slug":"test-endpoint"
            }
        
        responce = await client.post('/categories/', json = payload, headers = test_admin_auth_header)
        assert responce.status_code == 201

        bad_json_responce = await client.post('/categories/', json = {'test':'test'}, headers = test_admin_auth_header)
        assert bad_json_responce.status_code == 422

        bad_auth_responce = await client.post('/categories/', json = payload, headers = test_auth_header)
        assert bad_auth_responce.status_code == 403

    async def test_get_all_categories(self, client, test_category):

        responce = await client.get('/categories/')
        assert responce.status_code == 200
        data = responce.json()
        assert isinstance(data, list) and data[0] != []

    async def test_get_category_by_id(self, client, test_category):

        responce = await client.get(f'/categories/id/{test_category.id}')
        assert responce.status_code == 200
        data = responce.json()
        assert data['id'] == test_category.id

        bad_responce = await client.get(f'/categories/id/999')
        assert bad_responce.status_code == 404

    async def test_get_category_by_slug(self, client, test_category):
        
        responce = await client.get(f'/categories/{test_category.slug}')
        assert responce.status_code == 200
        data = responce.json()
        assert data['slug'] == test_category.slug

        bad_responce = await client.get(f'/categories/bad-slug')
        assert bad_responce.status_code == 404

    async def test_update_category(self, client, test_category, test_admin_auth_header, test_auth_header):
        payload = {
            "title":"test_update",
            "slug":"test-update"
            }
        
        responce = await client.put(f'/categories/id/{test_category.id}', json = payload, headers = test_admin_auth_header)
        assert responce.status_code == 200

        bad_json_responce = await client.put('/categories/id/{test_category.id}', json = {'test':'test'}, headers = test_admin_auth_header)
        assert bad_json_responce.status_code == 422

        bad_id_responce = await client.put('/categories/id/999', json = {"title":"bad_end_test"}, headers = test_admin_auth_header)
        assert bad_id_responce.status_code == 404

        bad_auth_responce = await client.put('/categories/id/{test_category.id}', json = payload, headers = test_auth_header)
        assert bad_auth_responce.status_code == 403

    async def test_delete_category(self, client, test_category, test_admin_auth_header, test_auth_header):

        bad_auth_responce = await client.delete(f'/categories/id/{test_category.id}', headers = test_auth_header)
        assert bad_auth_responce.status_code == 403

        bad_id_responce = await client.delete(f'/categories/id/999', headers = test_admin_auth_header)
        assert bad_id_responce.status_code == 404

        responce = await client.delete(f'/categories/id/{test_category.id}', headers = test_admin_auth_header)
        assert responce.status_code == 200
        data = responce.json()
        assert data['id'] == test_category.id






@pytest.mark.asyncio
class TestProductEndpoints:

    async def test_create_product(self, client, test_admin_auth_header, test_auth_header, test_category):
        
        payload = {
            "title":"test_endpoint",
            "category_id": str(test_category.id),
            "price": "1.00",
            "description":"desc",
            "image":"test root"
            }
        
        responce = await client.post('/products/', json = payload, headers = test_admin_auth_header)
        assert responce.status_code == 201

        bad_json_responce = await client.post('/products/', json = {'test':'test'}, headers = test_admin_auth_header)
        assert bad_json_responce.status_code == 422

        bad_auth_responce = await client.post('/products/', json = payload, headers = test_auth_header)
        assert bad_auth_responce.status_code == 403

    async def test_get_all_products(self, client, test_product):

        responce = await client.get('/products/')
        assert responce.status_code == 200
        data = responce.json()
        assert isinstance(data, list) and data[0] != []

    async def test_get_product_by_id(self, client, test_product):

        responce = await client.get(f'/products/id/{test_product.id}')
        assert responce.status_code == 200
        data = responce.json()
        assert data['id'] == test_product.id

        bad_responce = await client.get(f'/products/id/999')
        assert bad_responce.status_code == 404

    async def test_get_product_by_category(self, client, test_category, test_product):
        
        responce = await client.get(f'/products/{test_category.slug}')
        assert responce.status_code == 200
        data = responce.json()
        assert isinstance(data, list) and data[0] != []
    
        bad_responce = await client.get(f'/products/bad-slug')
        assert bad_responce.status_code == 404

    async def test_get_update_product(self, client, test_product, test_admin_auth_header, test_auth_header):

        payload = {
            "title":"test_update",
            "price": "2.00",
            "description":"desc_update",
            }
        
        responce = await client.put(f'/products/{test_product.id}', json = payload, headers = test_admin_auth_header)
        assert responce.status_code == 200

        bad_json_responce = await client.put('/products/{test_product.id}', json = {'test':'test'}, headers = test_admin_auth_header)
        assert bad_json_responce.status_code == 422

        bad_id_responce = await client.put('/products/999', json = {"title":"bad_end_test"}, headers = test_admin_auth_header)
        assert bad_id_responce.status_code == 404

        bad_auth_responce = await client.put('/products/{test_product.id}', json = payload, headers = test_auth_header)
        assert bad_auth_responce.status_code == 403

    async def test_delete_product(self, client, test_product, test_admin_auth_header, test_auth_header):

        bad_auth_responce = await client.delete(f'/products/{test_product.id}', headers = test_auth_header)
        assert bad_auth_responce.status_code == 403

        bad_id_responce = await client.delete(f'/products/999', headers = test_admin_auth_header)
        assert bad_id_responce.status_code == 404

        responce = await client.delete(f'/products/{test_product.id}', headers = test_admin_auth_header)
        assert responce.status_code == 200
        data = responce.json()
        assert data['id'] == test_product.id