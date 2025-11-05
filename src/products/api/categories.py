from fastapi import APIRouter, status

from src.products.dependencies import CategoryServiceDep
from src.products.schemas import CategoryIn, CategoryOut, CategoryUpdate

from uuid import UUID

router = APIRouter()

@router.get("", response_model=list[CategoryOut])
async def get_categories(service: CategoryServiceDep):
    return await service.get_all()

@router.get("/{category_id}", response_model=CategoryOut)
async def get_category(category_id: UUID, service: CategoryServiceDep):
    return await service.get_objects(id=category_id)
    
@router.post("", status_code=status.HTTP_201_CREATED, response_model=CategoryOut)
async def create_category(new_category: CategoryIn, service: CategoryServiceDep):
    return await service.create_object(new_category.model_dump())

@router.put("/{category_id}")
async def update_category(category_id: UUID, new_data: CategoryUpdate, service: CategoryServiceDep):
    return await service.update_objects(new_data.model_dump(),id=category_id)

@router.delete("/{category_id}")
async def delete_category(category_id: UUID, service: CategoryServiceDep):
    await service.delete_objects(id=category_id)
    return {"message": "deleted succesfully"}