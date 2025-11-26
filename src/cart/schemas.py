from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class AddToCartRequest(BaseModel):
    product_id: UUID
    quantity: int = Field(ge=1, default=1)


class UpdateCartItemRequest(BaseModel):
    quantity: int = Field(ge=1)


class CartItemProductOut(BaseModel):
    id: UUID
    name: str
    price_cents: int
    stock: int
    is_active: bool


class CartItemOut(BaseModel):
    id: UUID
    product: CartItemProductOut
    quantity: int
    subtotal: int


class CartOut(BaseModel):
    cart_id: UUID
    items: list[CartItemOut]
    total_items: int
    total_price_cents: int
    created_at: datetime
    updated_at: datetime
