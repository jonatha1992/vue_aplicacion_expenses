from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

Base = declarative_base()

# SQLAlchemy models
class CategoryDB(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    expenses = relationship("ExpenseDB", back_populates="category_rel")

class ExpenseDB(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    amount = Column(Float)
    date = Column(DateTime, default=datetime.utcnow)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category_rel = relationship("CategoryDB", back_populates="expenses")

# Pydantic models
class CategoryBase(BaseModel):
    name: str

    class Config:
        from_attributes = True

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True

class ExpenseCreate(BaseModel):
    description: str
    amount: float
    date: datetime
    category_id: int  # Cambiado de category: CategoryBase a category_id: int

    class Config:
        from_attributes = True

class Expense(ExpenseCreate):
    id: Optional[int] = None

# Modelo de usuario (SQLAlchemy)
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

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