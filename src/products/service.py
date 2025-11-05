from src.utils import CRUDRepository
from src.db import Base
from src.products.exception import ObjectNotFoundException, ObjectExistsException

from sqlalchemy.exc import IntegrityError

def check_objects(objects: list):
    if not objects:
            raise ObjectNotFoundException
    if len(objects) > 1:
        return objects
    else:
        return objects[0]

class CRUDService:
    def __init__(self, repository: CRUDRepository):
        self.repository = repository

    async def create_object(self, data: dict) -> Base:
        try:
            object = await self.repository.create(data=data)
        except IntegrityError:
            raise ObjectExistsException
        return object
    
    async def get_all(self) -> list[Base]:
        objects = await self.repository.get_all()
        return objects
    
    async def get_objects(self, **filter_by) -> list[Base] | Base:
        objects = await self.repository.find_one_or_many(**filter_by)
        return check_objects(objects)
        
    async def delete_objects(self, **filter_by) -> list[Base] | Base:
        objects = await self.repository.delete_one_or_more(**filter_by)
        return check_objects(objects)
        
    async def update_objects(self, data: dict, **filter_by) -> list[Base] | Base:
        objects = await self.repository.update_one_or_more(data, **filter_by)
        return check_objects(objects)
        
class CategoryService(CRUDService):
    pass

class ProductService(CRUDService):
    pass  
        