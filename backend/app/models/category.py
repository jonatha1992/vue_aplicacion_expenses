from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from .base import Base
from enum import Enum as PyEnum

class CategoryType(str, PyEnum):
    EXPENSE = "expense"
    INCOME = "income"

# SQLAlchemy models
class CategoryDB(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String, nullable=False)
    
    # Relaciones actualizadas
    expenses = relationship("ExpenseDB", back_populates="category")
    incomes = relationship("IncomeDB", back_populates="category")

# Pydantic models
class CategoryBase(BaseModel):
    name: str
    type: CategoryType

    model_config = ConfigDict(from_attributes=True)

class Category(CategoryBase):
    id: int
