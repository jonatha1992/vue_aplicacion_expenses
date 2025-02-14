from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

Base = declarative_base()

# SQLAlchemy model
class ExpenseDB(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    amount = Column(Float)
    date = Column(DateTime)
    category = Column(String)

# Pydantic model
class Expense(BaseModel):
    id: Optional[int] = None
    description: str
    amount: float
    date: datetime
    category: str
    
    class Config:
        from_attributes = True