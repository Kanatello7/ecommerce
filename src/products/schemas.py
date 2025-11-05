from pydantic import BaseModel, UUID4, Field
from uuid import UUID

from typing import Optional
from datetime import datetime

class CategoryIn(BaseModel):
    name: str = Field(min_length=1, max_length=130)

class CategoryUpdate(CategoryIn):
    pass 

class CategoryOut(CategoryIn):
    id: UUID
    slug: str 
    
    created_at: datetime
    updated_at: datetime

class ProductIn(BaseModel):
    name: str = Field(min_length=1, max_length=130)
    description: Optional[str | None] = None
    
    price_cents: int = Field(ge=0)
    stock: int = Field(ge=0)
    is_active: bool 

    category_id: UUID

class ProductUpdate(ProductIn):
    pass 

class ProductOut(ProductIn):
    id: UUID
    slug: str

    created_at: datetime
    updated_at: datetime
