from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import DateTime, text, func

from src.config import settings_db
from typing import AsyncGenerator, Annotated
from datetime import datetime, timezone

async_engine = create_async_engine(
    url=settings_db.DATABASE_URL,
)

async_session_maker = async_sessionmaker(bind=async_engine)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close() 

CreatedAt = Annotated[datetime, mapped_column(DateTime(timezone=True), server_default=func.now(), 
                                              nullable=False)]
UpdatedAt = Annotated[datetime, mapped_column(DateTime(timezone=True), server_default=func.now(), 
                                              nullable=False, 
                                              onupdate=datetime.now(tz=timezone.utc))]

class Base(DeclarativeBase):
    pass 