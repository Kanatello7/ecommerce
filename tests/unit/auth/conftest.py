import pytest

from src.auth.repository import AuthRepository, UserRepository
from src.auth.service import UserService, AuthService

@pytest.fixture()
def get_test_auth_repository(get_session):
    return AuthRepository(session=get_session)

@pytest.fixture()
def get_test_user_repository(get_session):
    return UserRepository(session=get_session)

@pytest.fixture()
def get_test_user_service(get_test_user_repository):
    return UserService(repository=get_test_user_repository)

@pytest.fixture()
def get_test_auth_service(get_test_auth_repository, get_test_user_service):
    return AuthService(repository=get_test_auth_repository,
                       user_service=get_test_user_service)