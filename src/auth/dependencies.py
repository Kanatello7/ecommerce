from typing import Annotated

from fastapi import Depends, Request

from src.auth.exceptions import (
    InvalidTokenException,
    NotAuthenticatedException,
    PermissionDeniedException,
)
from src.auth.models import User
from src.auth.repository import AuthRepository, UserRepository
from src.auth.service import AuthService, UserService
from src.db import AsyncSession, get_session


def get_auth_repository(session: Annotated[AsyncSession, Depends(get_session)]):
    return AuthRepository(session=session)


def get_user_repository(session: Annotated[AsyncSession, Depends(get_session)]):
    return UserRepository(session=session)


def get_user_service(
    repository: Annotated[UserRepository, Depends(get_user_repository)],
):
    return UserService(repository=repository)


def get_auth_service(
    repository: Annotated[AuthRepository, Depends(get_auth_repository)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return AuthService(repository=repository, user_service=user_service)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


def login_required(func):
    async def wrapper(request: Request, service: AuthServiceDep):
        token = request.cookies.get("access_token")

        if not token:
            raise NotAuthenticatedException

        payload = await service.decode_token(token)

        username = payload.get("sub")
        if not username:
            raise InvalidTokenException

        user = await service.user_service.get_user_by_username(username)
        return await func(current_user=user)

    return wrapper


async def get_current_user(request: Request, service: AuthServiceDep) -> User:
    """
    Dependency to get the current authenticated user from access token cookie.
    Raises NotAuthenticatedException if token is missing or invalid.
    """
    token = request.cookies.get("access_token")

    if not token:
        raise NotAuthenticatedException

    payload = await service.decode_token(token)

    username = payload.get("sub")
    if not username:
        raise InvalidTokenException

    user = await service.user_service.get_user_by_username(username)

    if not user:
        raise InvalidTokenException

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


async def get_current_admin_user(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise PermissionDeniedException
    return current_user


CurrentAdmin = Annotated[User, Depends(get_current_admin_user)]
