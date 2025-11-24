from src.db import Base, CreatedAt, UpdatedAt
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, ForeignKey, String, Enum as SQLEnum, CheckConstraint, Integer
from uuid import uuid4, UUID as UID
from enum import Enum

class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[UID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    order_id: Mapped[UID] = mapped_column(UUID(as_uuid=True),
                                           ForeignKey('orders.id', ondelete="RESTRICT"),
                                           unique=True, nullable=False, index=True)
    stripe_charge_id: Mapped[str | None] = mapped_column(String(280), unique=True, nullable=True)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)  # in cents
    currency: Mapped[str] = mapped_column(String(3), default="usd", nullable=False)
    status: Mapped[PaymentStatus] = mapped_column(SQLEnum(PaymentStatus),
                                                    default=PaymentStatus.PENDING,
                                                    nullable=False, index=True)
    
    order: Mapped["Order"] = relationship(back_populates="payment")

    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    __table_args__ = (
        CheckConstraint('amount > 0', name='check_payment_amount_positive'),
    )