# src/cart/repository.py
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.cart.models import Cart, CartItem
from src.utils import SqlAlchemyCRUDRepository


class CartRepository(SqlAlchemyCRUDRepository):
    model = Cart


class CartItemRepository(SqlAlchemyCRUDRepository):
    model = CartItem

    async def get_cart_items_with_products(self, cart_id):
        """Get all cart items with their associated products"""
        query = (
            select(self.model)
            .where(self.model.cart_id == cart_id)
            .options(joinedload(self.model.product))
        )
        result = await self.session.execute(query)
        return result.scalars().all()
