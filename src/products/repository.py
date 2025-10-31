from src.products.models import Product, Category
from src.utils import SqlAlchemyCRUDRepository

class CategoryRepository(SqlAlchemyCRUDRepository):
    model = Category

class ProductRepository(SqlAlchemyCRUDRepository):
    model = Product
