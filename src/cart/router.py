from uuid import UUID

from fastapi import APIRouter, status

from src.auth.dependencies import CurrentUser
from src.cart.dependencies import CartServiceDep
from src.cart.schemas import *

router = APIRouter()


@router.get("", response_model=CartOut)
async def get_cart(service: CartServiceDep, current_user=CurrentUser):
    """Get current user's cart with all items"""
    return await service.get_cart_with_items(current_user.id)


@router.post("/items", status_code=status.HTTP_201_CREATED)
async def add_to_cart(
    request: AddToCartRequest,
    service: CartServiceDep,
    current_user=CurrentUser,
):
    """Add product to cart"""
    await service.add_item_to_cart(
        current_user.id, request.product_id, request.quantity
    )
    return {"message": "Item added to cart"}


@router.put("/items/{cart_item_id}")
async def update_cart_item(
    cart_item_id: UUID,
    request: UpdateCartItemRequest,
    service: CartServiceDep,
    current_user=CurrentUser,
):
    """Update cart item quantity"""
    await service.update_item_quantity(current_user.id, cart_item_id, request.quantity)
    return {"message": "Cart item updated"}


@router.delete("/items/{cart_item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_cart(
    cart_item_id: UUID, service: CartServiceDep, current_user=CurrentUser
):
    """Remove item from cart"""
    await service.remove_item_from_cart(current_user.id, cart_item_id)


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def clear_cart(service: CartServiceDep, current_user=CurrentUser):
    """Clear all items from cart"""
    await service.clear_cart(current_user.id)
