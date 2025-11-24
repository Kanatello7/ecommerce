# src/orders/models.py
from src.db import Base, CreatedAt, UpdatedAt
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, ForeignKey, Integer, String, Enum as SQLEnum, CheckConstraint
from uuid import uuid4, UUID as UID
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[UID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UID] = mapped_column(UUID(as_uuid=True),
                                          ForeignKey('users.id', ondelete="RESTRICT"),
                                          nullable=False, index=True)
    status: Mapped[OrderStatus] = mapped_column(SQLEnum(OrderStatus), 
                                                 default=OrderStatus.PENDING, 
                                                 nullable=False, index=True)
    total_amount: Mapped[int] = mapped_column(Integer, nullable=False)  # in cents
    
    user: Mapped["User"] = relationship()
    items: Mapped[list["OrderItem"]] = relationship(back_populates="order", cascade="all, delete-orphan")
    payment: Mapped["Payment"] = relationship(back_populates="order", uselist=False)

    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    __table_args__ = (
        CheckConstraint('total_amount >= 0', name='check_total_amount_positive'),
    )

class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[UID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    order_id: Mapped[UID] = mapped_column(UUID(as_uuid=True),
                                           ForeignKey('orders.id', ondelete="CASCADE"),
                                           nullable=False, index=True)
    product_id: Mapped[UID] = mapped_column(UUID(as_uuid=True),
                                             ForeignKey('products.id', ondelete="RESTRICT"),
                                             nullable=False, index=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    product_name: Mapped[str] = mapped_column(String(130), nullable=False)  # snapshot
    product_price: Mapped[int] = mapped_column(Integer, nullable=False)  # snapshot in cents
    
    order: Mapped["Order"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship()

    __table_args__ = (
        CheckConstraint('quantity > 0', name='check_order_quantity_positive'),
        CheckConstraint('product_price >= 0', name='check_product_price_positive'),
    )