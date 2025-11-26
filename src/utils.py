from abc import ABC, abstractmethod

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDRepository(ABC):
    @abstractmethod
    async def create(self):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self):
        raise NotImplementedError

    @abstractmethod
    async def find_one_or_many(self):
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

    async def get_all(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def find_one_or_many(self, *filter, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def create(self, data: dict):
        obj = self.model(**data)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj
        # CORE style
        # stmt = insert(self.model).values(**data).returning(self.model)
        # result = await self.session.execute(stmt)
        # obj = result.scalar_one()

    async def update_one_or_more(self, data, **filter_by):
        if not filter_by:
            raise ValueError("filter_by cannot be empty")
        if not data:
            raise ValueError("data cannot be empty")

        stmt = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(stmt)
        objects = result.scalars().all()
        for obj in objects:
            for key, value in data.items():
                setattr(obj, key, value)

        await self.session.commit()
        for obj in objects:
            await self.session.refresh(obj)
        return objects
        # CORE style (faster but doesn't trigger events)
        # stmt = update(self.model).values(**data).filter_by(**filter_by).returning(self.model)
        # result = await self.session.execute(stmt)
        # await self.session.commit()
        # return result.scalars().all()

    async def delete_one_or_more(self, **filter_by):
        if not filter_by:
            raise ValueError("filter_by cannot be empty")

        stmt = delete(self.model).filter_by(**filter_by).returning(self.model)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalars().all()
