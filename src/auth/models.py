from src.db import Base, CreatedAt, UpdatedAt

from sqlalchemy.orm import Mapped, mapped_column, relationship 
from sqlalchemy import String, DateTime, Boolean, UUID 

from datetime import datetime
from uuid import uuid4, UUID as UID


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[UID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    first_name: Mapped[str] = mapped_column(String(130), nullable=False)
    last_name: Mapped[str] = mapped_column(String(130), nullable=False)
    email: Mapped[str] = mapped_column(String(130), nullable=False, unique=True) 

    last_login: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=None, nullable=True)
    password: Mapped[str] = mapped_column(String, nullable=False) 
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[CreatedAt] 
    updated_at: Mapped[UpdatedAt] 

    cart: Mapped["Cart"] = relationship(back_populates="user", uselist=False)

    def __str__(self):
        return f"{self.id}:{self.first_name} {self.last_name} email:{self.email}"




