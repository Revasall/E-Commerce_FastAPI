from fastapi import status, HTTPException


# Common Errors
class ObjectNotFoundError(HTTPException):
    def __init__(self, object_name:str = 'Object'):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'{object_name} not found.'
        )

class ObjectAlreadyExistsError(HTTPException):
    def __init__(self, object_name: str = 'Object'):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'{object_name} already exists'
        )

class ObjectCreateError(HTTPException):
    def __init__(self, object_name: str = 'Object'):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'{object_name} create error'
        )

class PermissionDeniedError(HTTPException):
    def __init__(self, message: str = "You don't have permission to perform this action."):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message
        )

class InvalidDataError(HTTPException):
    def __init__(self, message: str = "Invalid or incomplete data provided."):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=message
        )

# Auth Errors

class InvalidCredentialsError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password.',
            headers={"WWW-Authenticate": "Bearer"}
        )

class InvalidTokenTypeError(HTTPException):
    def __init__(self, token_type: str, expected_type:str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'The received token type ({token_type}) does not match the expected ({expected_type}).',
            headers={"WWW-Authenticate": "Bearer"}
        )

class InvalidTokenError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid jwt token.',
            headers={"WWW-Authenticate": "Bearer"}
        )

class ExpiredTokenError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token has expired.',
            headers={"WWW-Authenticate": "Bearer"}
        )


# Users Errors 

class UserAlreadyExistsError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail='User with this username or email already exists.'
        )

class UserNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = 'User not found.'
            )
class UserCreateError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail='failed to create new user'
        )
#Tasks Errors

class TaskNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = 'Task not found.')
        
class TaskAccessDeniedError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to modify this task."
        )