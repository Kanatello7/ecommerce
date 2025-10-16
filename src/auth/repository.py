from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from src.auth.models import User

class AuthRepository:
    def __init__(self, session: AsyncSession):
        self.session = session 

class UserRepository:
    model = User

    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def find_one_or_more(self, *filter, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()
    
    async def create(self, data: dict):
        stmt = insert(self.model).values(**data).returning(self.model)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()
    
