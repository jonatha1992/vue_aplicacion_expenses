from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .base import Base


# Modelo de usuario (SQLAlchemy)
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expenses = relationship("ExpenseDB", back_populates="user")  # Nueva relación con gastos

# Esquema de usuario (Pydantic)
class User(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Para ingreso/registro, puedes definir esquemas adicionales (p.ej., UserCreate)
class UserCreate(BaseModel):
    username: str
    email: str
    password: str