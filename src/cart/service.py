from uuid import UUID

from src.cart.exceptions import *
from src.cart.models import Cart, CartItem
from src.cart.repository import CartItemRepository, CartRepository
from src.products.repository import ProductRepository


class CartService:
    def __init__(
        self,
        cart_repo: CartRepository,
        cart_item_repo: CartItemRepository,
        product_repo: ProductRepository,
    ):
        self.cart_repo = cart_repo
        self.cart_item_repo = cart_item_repo
        self.product_repo = product_repo

    async def get_or_create_cart(self, user_id: UUID) -> Cart:
        """Get user's cart or create if doesn't exist"""
        carts = await self.cart_repo.find_one_or_many(user_id=user_id)
        if carts:
            return carts[0]

        cart_data = {"user_id": user_id}
        return await self.cart_repo.create(cart_data)

    async def get_cart_with_items(self, user_id: UUID) -> dict:
        """Get cart with all items and calculated totals"""
        cart = await self.get_or_create_cart(user_id)
        items = await self.cart_item_repo.get_cart_items_with_products(cart.id)

        total_price = sum(item.product.price_cents * item.quantity for item in items)

        return {
            "cart_id": cart.id,
            "items": [
                {
                    "id": item.id,
                    "product": {
                        "id": item.product.id,
                        "name": item.product.name,
                        "price_cents": item.product.price_cents,
                        "stock": item.product.stock,
                        "is_active": item.product.is_active,
                    },
                    "quantity": item.quantity,
                    "subtotal": item.product.price_cents * item.quantity,
                }
                for item in items
            ],
            "total_items": sum(item.quantity for item in items),
            "total_price_cents": total_price,
            "created_at": cart.created_at,
            "updated_at": cart.updated_at,
        }

    async def add_item_to_cart(
        self, user_id: UUID, product_id: UUID, quantity: int = 1
    ) -> CartItem:
        """Add product to cart or update quantity if exists"""
        if quantity <= 0:
            raise InvalidQuantityException

        # Verify product exists and is available
        products = await self.product_repo.find_one_or_many(id=product_id)
        if not products:
            raise ProductNotFoundException

        product = products[0]
        if not product.is_active:
            raise ProductNotAvailableException

        if product.stock < quantity:
            raise InsufficientStockException

        # Get or create cart
        cart = await self.get_or_create_cart(user_id)

        # Check if item already exists in cart
        existing_items = await self.cart_item_repo.find_one_or_many(
            cart_id=cart.id, product_id=product_id
        )

        if existing_items:
            # Update existing item
            item = existing_items[0]
            new_quantity = item.quantity + quantity

            if product.stock < new_quantity:
                raise InsufficientStockException

            updated = await self.cart_item_repo.update_one_or_more(
                {"quantity": new_quantity}, id=item.id
            )
            return updated[0] if isinstance(updated, list) else updated
        else:
            # Create new item
            item_data = {
                "cart_id": cart.id,
                "product_id": product_id,
                "quantity": quantity,
            }
            return await self.cart_item_repo.create(item_data)

    async def update_item_quantity(
        self, user_id: UUID, cart_item_id: UUID, quantity: int
    ) -> CartItem:
        """Update quantity of a cart item"""
        if quantity <= 0:
            raise InvalidQuantityException

        cart = await self.get_or_create_cart(user_id)

        # Verify item belongs to user's cart
        items = await self.cart_item_repo.find_one_or_many(
            id=cart_item_id, cart_id=cart.id
        )

        if not items:
            raise CartItemNotFoundException

        item = items[0]

        # Check stock availability
        products = await self.product_repo.find_one_or_many(id=item.product_id)
        if not products:
            raise ProductNotFoundException

        product = products[0]
        if product.stock < quantity:
            raise InsufficientStockException

        updated = await self.cart_item_repo.update_one_or_more(
            {"quantity": quantity}, id=cart_item_id
        )
        return updated[0] if isinstance(updated, list) else updated

    async def remove_item_from_cart(self, user_id: UUID, cart_item_id: UUID) -> None:
        """Remove item from cart"""
        cart = await self.get_or_create_cart(user_id)

        # Verify item belongs to user's cart
        items = await self.cart_item_repo.find_one_or_many(
            id=cart_item_id, cart_id=cart.id
        )

        if not items:
            raise CartItemNotFoundException

        await self.cart_item_repo.delete_one_or_more(id=cart_item_id)

    async def clear_cart(self, user_id: UUID) -> None:
        """Remove all items from cart"""
        cart = await self.get_or_create_cart(user_id)
        await self.cart_item_repo.delete_one_or_more(cart_id=cart.id)

    async def validate_cart_for_checkout(self, user_id: UUID) -> dict:
        """Validate cart items before checkout"""
        cart_data = await self.get_cart_with_items(user_id)

        if not cart_data["items"]:
            raise EmptyCartException

        errors = []
        for item in cart_data["items"]:
            product = item["product"]

            if not product["is_active"]:
                errors.append(
                    {
                        "product_id": product["id"],
                        "product_name": product["name"],
                        "error": "Product is no longer available",
                    }
                )
            elif product["stock"] < item["quantity"]:
                errors.append(
                    {
                        "product_id": product["id"],
                        "product_name": product["name"],
                        "error": f"Insufficient stock. Available: {product['stock']}, requested: {item['quantity']}",
                    }
                )

        if errors:
            raise CartValidationException(errors)

        return cart_data
