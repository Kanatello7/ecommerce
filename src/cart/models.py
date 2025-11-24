# src/cart/models.py
from src.db import Base, CreatedAt, UpdatedAt
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, ForeignKey, Integer, UniqueConstraint, CheckConstraint
from uuid import uuid4, UUID as UID

class Cart(Base):
    __tablename__ = "carts"

    id: Mapped[UID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UID] = mapped_column(UUID(as_uuid=True),
                                          ForeignKey('users.id', ondelete="CASCADE"),
                                          unique=True, nullable=False, index=True)
    
    user: Mapped["User"] = relationship(back_populates="cart")
    items: Mapped[list["CartItem"]] = relationship(back_populates="cart", cascade="all, delete-orphan")

    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

class CartItem(Base):
    __tablename__ = "cart_items"

    id: Mapped[UID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    cart_id: Mapped[UID] = mapped_column(UUID(as_uuid=True),
                                          ForeignKey('carts.id', ondelete="CASCADE"),
                                          nullable=False, index=True)
    product_id: Mapped[UID] = mapped_column(UUID(as_uuid=True),
                                             ForeignKey('products.id', ondelete="CASCADE"),
                                             nullable=False, index=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    
    cart: Mapped["Cart"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship()

    added_at: Mapped[CreatedAt]

    __table_args__ = (
        UniqueConstraint('cart_id', 'product_id', name='unique_cart_product'),
        CheckConstraint('quantity > 0', name='check_quantity_positive'),
    )