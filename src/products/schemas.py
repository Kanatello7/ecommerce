from pydantic import BaseModel, UUID4
from uuid import UUID

from typing import Optional
from datetime import datetime

class CategoryOut(BaseModel):
    pass 

class ProductOut(BaseModel):
    id: UUID
    name: str
    slug: str
    description: Optional[str | None] = None 
    
    price_cents: int
    stock: int
    is_active: bool

    created_at: datetime
    updated_at: datetime

    category_id: UUID
    category: 