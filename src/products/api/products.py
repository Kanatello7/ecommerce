from fastapi import APIRouter, status

from src.products.dependencies import ProductServiceDep
from src.products.schemas import ProductIn, ProductOut, ProductUpdate

from uuid import UUID

router = APIRouter()

@router.get("", response_model=list[ProductOut])
async def get_products(service: ProductServiceDep):
    return await service.get_all()

@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: UUID, service: ProductServiceDep):
    return await service.get_objects(id=product_id)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=ProductOut)
async def create_product(new_product: ProductIn, service: ProductServiceDep):
    return await service.create_object(new_product.model_dump())

@router.put("/{product_id}", response_model=ProductOut)
async def update_product(product_id: UUID, new_data: ProductUpdate, service: ProductServiceDep):
    return await service.update_objects(new_data.model_dump(),id=product_id)

@router.delete("/{product_id}")
async def delete_product(product_id: UUID, service: ProductServiceDep):
    await service.delete_objects(id=product_id)
    return {"message": "deleted succesfully"}