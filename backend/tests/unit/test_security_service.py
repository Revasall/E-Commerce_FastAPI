import pytest
import jwt

from datetime import timedelta
from ...app.core.security import SecurityService
from ...app.core.exceptions import InvalidTokenError, InvalidTokenTypeError, ExpiredTokenError
from ...app.config.config import settings
from ...app.models.user import User




service = SecurityService()

def test_passport_hash_an_verify():
    password = 'password'
    hashed = service.get_password_hash(password)
    
    #Test hashing password
    assert hashed != password
    assert len(hashed) > 20

    #Test verify password
    assert service.verify_password(password, hashed) is True
    assert service.verify_password('wrong_pass', hashed) is False


def test_create_jwt_token():
    payload = {
            'sub': '123',
            'email': 'example@example.com',
            'role': 'user',
            'token_type': 'access'
        }
    token = service.create_jwt(payload=payload, expires_delta=timedelta(minutes=5))
    decoded = jwt.decode(token, service.SECRET_KEY, algorithms=[service.ALGORITHM])

    assert decoded['sub'] == '123'
    assert decoded['email'] == 'example@example.com'
    assert decoded['role'] == 'user'
    assert decoded['token_type'] == 'access'
    assert 'exp' in decoded

def test_create_access_and_refresh_tokens():
    user = User(id=1, 
                username='john123', 
                email='john_doe@test.com')
    access = service.create_access_token(user)
    refresh = service.create_refresh_token(user)

    d_access = jwt.decode(access, service.SECRET_KEY, algorithms=[service.ALGORITHM])
    d_refresh = jwt.decode(refresh, service.SECRET_KEY, algorithms=[service.ALGORITHM])

    assert d_access['token_type'] == 'access'
    assert d_refresh['token_type'] == 'refresh'
    assert d_access['sub'] == '1'


def test_decode_jwt_token():

    #Valid token
    payload = {'sub': '1', 'token_type': 'access'}
    token = service.create_jwt(payload, timedelta(minutes=5))
    decoded = service.decode_jwt_token(token, expected_type='access')

    assert decoded['sub'] == '1'

    #Invalid token
    payload = {'sub': '1', 'token_type': 'refresh'}
    token = service.create_jwt(payload, timedelta(minutes=5))
    with pytest.raises(InvalidTokenTypeError):
        service.decode_jwt_token(token, expected_type='access')

    #Expired token
    payload = {'sub': '1', 'token_type': 'access'}
    token = service.create_jwt(payload, timedelta(minutes=-1))
    with pytest.raises(ExpiredTokenError):
        service.decode_jwt_token(token, expected_type='access')

    #Invalid signature
    payload = {'sub': '1', 'token_type': 'access'}
    token = jwt.encode(payload=payload, key='wrong_key', algorithm=service.ALGORITHM)
    with pytest.raises(InvalidTokenError):
        service.decode_jwt_token(token, expected_type='access')


# @pytest.mark.asyncio 
# async def test_get_current_user(session):

#     user = session.
#     token = service.create_access_token(user)
#     result = await service.get_current_user(token, session=session)
#     assert result.id == user.id and  result.username == user.username

#     invalid_token = 'invalid_token'
#     with pytest.raises(InvalidTokenError):
#         await service.get_current_user(invalid_token, session=session)
    

