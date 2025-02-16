from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .base import Base


# SQLAlchemy models
class CategoryDB(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    expenses = relationship("ExpenseDB", back_populates="category_rel")

# Pydantic models
class CategoryBase(BaseModel):
    name: str

    class Config:
        from_attributes = True

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True
