import pytest

from src.auth.repository import AuthRepository, UserRepository
from src.auth.service import UserService, AuthService
from src.auth.models import User

@pytest.fixture
def sample_user():
    return User(id=1, first_name="tom", last_name="holland", email="tom@gmail.com", password="hashed_password")

@pytest.fixture
def sample_user_data():
    return {"id": 1,
            "fist_name": "tom",
            "last_name": "holland",
            "email": "tom@gmail.com",
            "password": "plain_password"}

@pytest.fixture()
def test_auth_repository(get_session):
    return AuthRepository(session=get_session)

@pytest.fixture()
def test_user_repository(get_session):
    return UserRepository(session=get_session)

@pytest.fixture()
def test_user_service(test_user_repository):
    return UserService(repository=test_user_repository)

@pytest.fixture()
def test_auth_service(test_auth_repository, test_user_service):
    return AuthService(repository=test_auth_repository,
                       user_service=test_user_service)