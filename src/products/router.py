from fastapi import APIRouter 
from src.products.dependencies import CategoryServiceDep, ProductServiceDep

router = APIRouter()

@router.get("")
async def get_products(service: ProductServiceDep):
    return service.get_products()

