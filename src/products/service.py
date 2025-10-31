from src.products.repository import CategoryRepository, ProductRepository
from src.products.models import Product, Category

class CategoryService:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository
    
class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    async def create_product(self, data: dict) -> Product:
        product = await self.repository.create(data=data)
        return product
    
    async def get_products(self) -> list[Product]:
        products = await self.repository.get_all()
        return products
    
    async def delete_product(self, id) -> list[Product]:
        product = await self.repository.delete_one_or_more(id=id)
        return product

    async def update_products(self, data: dict, **filter_by) -> list[Product]:
        products = await self.repository.update_one_or_more(data, **filter_by)
        return products

        