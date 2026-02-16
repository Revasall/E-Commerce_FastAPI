import pytest

from backend.app.models.user import User


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


# @pytest.mark.asyncio
# class TestCategoryEndpoints:

#     async def 
