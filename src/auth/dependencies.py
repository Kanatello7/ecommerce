from fastapi import Depends, Request

from src.auth.repository import AuthRepository, UserRepository
from src.auth.service import AuthService, UserService
from src.db import get_session, AsyncSession
from src.auth.exceptions import InvalidTokenException, NotAuthenticatedExceptino

from typing import Annotated, Optional

def get_auth_repository(session: Annotated[AsyncSession, Depends(get_session)]):
    return AuthRepository(session=session)

def get_user_repository(session: Annotated[AsyncSession, Depends(get_session)]):
    return UserRepository(session=session)

def get_user_service(repository: Annotated[UserRepository, Depends(get_user_repository)]):
    return UserService(repository=repository)

def get_auth_service(repository: Annotated[AuthRepository, Depends(get_auth_repository)], user_service: Annotated[UserService, Depends(get_user_service)]):
    return AuthService(repository=repository, user_service=user_service)

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]

def login_required(func):
    async def wrapper(request: Request, service: AuthServiceDep):
        token = request.cookies.get("access_token")

        if not token:
            raise NotAuthenticatedExceptino

        payload = await service.decode_token(token)

        username = payload.get("sub")
        if not username:
            raise InvalidTokenException

        user = await service.user_service.get_user_by_username(username)
        return await func(current_user=user)

    return wrapper

