from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .base import Base


class ExpenseDB(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    amount = Column(Float)
    date = Column(DateTime, default=datetime.utcnow)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category_rel = relationship("CategoryDB", back_populates="expenses")

# Pydantic models


class ExpenseCreate(BaseModel):
    description: str
    amount: float
    date: datetime
    category_id: int  # Cambiado de category: CategoryBase a category_id: int

    class Config:
        from_attributes = True

class Expense(ExpenseCreate):
    id: Optional[int] = None
