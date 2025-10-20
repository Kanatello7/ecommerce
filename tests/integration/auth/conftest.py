from src.auth.service import UserService, AuthService
from src.auth.repository import UserRepository, AuthRepository
from src.auth.dependencies import get_auth_repository, get_user_repository, get_user_service, get_auth_service
from src.main import app

import pytest 
from httpx import AsyncClient, ASGITransport

transport = ASGITransport(app=app)

@pytest.fixture(scope='function')
def override_dependencies(get_session):
    app.dependency_overrides[get_auth_repository] = lambda: AuthRepository(session=get_session)
    app.dependency_overrides[get_user_repository] = lambda: UserRepository(session=get_session) 
    app.dependency_overrides[get_user_service] = lambda: UserService(repository=UserRepository(session=get_session)) 
    app.dependency_overrides[get_auth_service] = lambda: AuthService(repository=AuthRepository(session=get_session),
                                                                     user_service=UserService(repository=UserRepository(session=get_session)))
    yield
    app.dependency_overrides = {} 

@pytest.fixture
async def async_client(override_dependencies):
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client 



