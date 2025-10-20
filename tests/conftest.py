import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.db import Base

from typing import AsyncGenerator

TEST_DB_URL = 'sqlite+aiosqlite:///:memory:'
test_engine = create_async_engine(url=TEST_DB_URL)
session_factory = async_sessionmaker(bind=test_engine, expire_on_commit=False)

@pytest.fixture(scope='session')
async def setup_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='function')
async def get_session(setup_database) -> AsyncGenerator[AsyncSession, None]:
    connection = await test_engine.connect()
    transaction = await connection.begin()
    
    session = AsyncSession(bind=connection, expire_on_commit=False)
    
    yield session
    
    await session.close()
    await transaction.rollback()
    await connection.close()