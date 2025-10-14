from src.db import Base 
from sqlalchemy.orm import Mapped, MappedColumn 
from sqlalchemy import Integer, String, DateTime
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = MappedColumn(Integer, primary_key=True)
    first_name: Mapped[str] = MappedColumn(String(130), nullable=False)
    last_name: Mapped[str] = MappedColumn(String(130), nullable=False)
    email: Mapped[str] = MappedColumn(String(130), nullable=False, unique=True) 

    last_login: Mapped[datetime] = MappedColumn(DateTime(timezone=True), default=None)
    password: Mapped[str] = MappedColumn(String, nullable=False) 

    def __str__(self):
        return f"{self.id}:{self.first_name} {self.last_name} email:{self.email}"




