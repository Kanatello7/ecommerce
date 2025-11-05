from src.db import Base, CreatedAt, UpdatedAt
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, UUID, Integer, Boolean, ForeignKey, CheckConstraint, Text, event

from uuid import uuid4, UUID as UID
import re 

def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub("[^a-z0-9]+", "-", value)
    return value.strip('-')

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[UID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(130), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(String(130), nullable=False, unique=True)

    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    products: Mapped[list["Product"]] = relationship(back_populates="category", passive_deletes=False)

class Product(Base):
    __tablename__ = "products"

    id: Mapped[UID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(130), nullable=False)
    slug: Mapped[str] = mapped_column(String(280), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    price_cents: Mapped[int] = mapped_column(Integer, nullable=False, )
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    category_id: Mapped[UID] = mapped_column(ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False, index=True)    
    category: Mapped["Category"] = relationship(back_populates="products")

    __table_args__ = (
        CheckConstraint('price_cents >= 0', name="check_price_cents_positive"),
        CheckConstraint("stock >=0", name="check_stock_non_negative")
    )

@event.listens_for(Category, "before_insert")
@event.listens_for(Category, "before_update")
def generate_category_slug(mapper, connection, target):
    target.slug = slugify(target.name)

@event.listens_for(Product, "before_insert")
@event.listens_for(Product, "before_update")
def generate_category_slug(mapper, connection, target):
    target.slug = slugify(target.name)