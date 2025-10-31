from abc import ABC, abstractmethod
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

class CRUDRepository(ABC):
    @abstractmethod
    async def create(self):
        raise NotImplementedError
    
    @abstractmethod
    async def find_one(self):
        raise NotImplementedError
    
    @abstractmethod
    async def find_many(self):
        raise NotImplementedError
    
    @abstractmethod
    async def get_all(self):
        raise NotImplementedError

    @abstractmethod
    async def update_one_or_more(self):
        raise NotImplementedError
    
    @abstractmethod
    async def delete_one_or_more(self):
        raise NotImplementedError

class SqlAlchemyCRUDRepository(CRUDRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def find_one(self, *filter, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()
    
    async def find_many(self, *filter, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_all(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def create(self, data: dict):
        stmt = insert(self.model).values(**data).returning(self.model)
        result = await self.session.execute(stmt)
        await self.session.commit()
        obj = result.scalar_one()
        await self.session.refresh(obj)
        return obj


    async def update_one_or_more(self, data, **filter_by):
        if not filter_by:
            raise ValueError("filter_by cannot be empty")
        
        stmt = update(self.model).values(**data).filter_by(**filter_by).returning(self.model)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalars().all()

    async def delete_one_or_more(self, **filter_by):
        stmt = delete(self.model).filter_by(**filter_by).returning(self.model)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalars().all()
