from src.db import Base, CreatedAt, UpdatedAt

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, ForeignKey

from uuid import uuid4, UUID as UID

class Cart(Base):
    __tablename__ = "carts"

    id: Mapped[UID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UID] = mapped_column(UUID(as_uuid=True),
                                          ForeignKey('users.id', ondelete="CASCADE"),
                                          unique=True, nullable=False)
    user: Mapped["User"] = relationship(back_populates="cart")

    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]