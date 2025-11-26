from typing import Annotated

from fastapi import Depends

from src.cart.repository import CartItemRepository, CartRepository
from src.cart.service import CartService
from src.db import AsyncSession, get_session
from src.products.dependencies import get_product_repository
from src.products.repository import ProductRepository


async def get_cart_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CartRepository:
    return CartRepository(session=session)


async def get_cart_item_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CartItemRepository:
    return CartItemRepository(session=session)


async def get_cart_service(
    cart_repo: Annotated[CartRepository, Depends(get_cart_repository)],
    cart_item_repo: Annotated[CartItemRepository, Depends(get_cart_item_repository)],
    product_repo: Annotated[ProductRepository, Depends(get_product_repository)],
) -> CartService:
    return CartService(
        cart_repo=cart_repo, cart_item_repo=cart_item_repo, product_repo=product_repo
    )


CartServiceDep = Annotated[CartService, Depends(get_cart_service)]
