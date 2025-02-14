from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

Base = declarative_base()

# Modelo SQLAlchemy para Category
class CategoryDB(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    # Relación con expenses
    expenses = relationship("ExpenseDB", back_populates="category_rel")

# Modelo SQLAlchemy para Expense
class ExpenseDB(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    amount = Column(Float)
    date = Column(DateTime, default=datetime.utcnow)
    # Guardamos la categoría como clave foránea
    category_id = Column(Integer, ForeignKey("categories.id"))
    
    # Relación con Category
    category_rel = relationship("CategoryDB", back_populates="expenses")

# Esquema Pydantic para Category
class Category(BaseModel):
    id: Optional[int] = None
    name: str

    class Config:
        from_attributes = True

# Esquema Pydantic para Expense  
class Expense(BaseModel):
    id: Optional[int] = None
    description: str
    amount: float
    date: datetime
    category: Optional[Category] = None   # Puede ser opcional

    class Config:
        from_attributes = True

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