from fastapi import Depends
from typing import Annotated
from src.db import get_session, AsyncSession

from src.products.repository import CategoryRepository, ProductRepository
from src.products.service import CategoryService, ProductService

async def get_category_repository(session: Annotated[AsyncSession, Depends(get_session)]):
    return CategoryRepository(session=session)

async def get_product_repository(session: Annotated[AsyncSession, Depends(get_session)]):
    return ProductRepository(session=session)

async def get_category_service(repository: Annotated[CategoryRepository, Depends(get_category_repository)]):
    return CategoryService(repository=repository)

async def get_product_service(repository: Annotated[ProductRepository, Depends(get_product_repository)]):
    return ProductService(repository=repository)

CategoryServiceDep = Annotated[CategoryService, Depends(get_category_service)]
ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]
