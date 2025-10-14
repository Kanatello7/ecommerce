from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from config import settings_db
from typing import AsyncGenerator

async_engine = create_async_engine(
    url=settings_db.DATABASE_URL,
)

async_session_maker = async_sessionmaker(bind=async_engine)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
        except:
            await session.close() 

class Base(DeclarativeBase):
    pass 