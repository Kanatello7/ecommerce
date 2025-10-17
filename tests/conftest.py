import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.main import app 
from src.auth.service import *
from src.auth.repository import *
from src.auth.dependencies import AuthServiceDep

from typing import AsyncGenerator

TEST_DB_URL = 'sqlite+aiosqlite:///:memory:'
test_engine = create_async_engine(url=TEST_DB_URL)
session_factory = async_sessionmaker(bind=test_engine)

@pytest.fixture(scope='session')
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        try:
            yield session
        finally:
            await session.close()

@pytest.fixture(scope='session')
def override_get_session(get_session):
    async def _get_test_session() -> AsyncGenerator[AsyncSession, None]:
        yield get_session

    # Override the dependency that provides the session in AuthService/AuthRepository
    app.dependency_overrides[AuthServiceDep] = lambda: AuthService(
        AuthRepository(get_session),
        user_service=UserService(UserRepository(get_session))
    )
    yield
    # Clean up the override after tests
    app.dependency_overrides = {}
    