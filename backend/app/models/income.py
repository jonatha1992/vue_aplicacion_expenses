from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from .base import Base

class IncomeDB(Base):
    __tablename__ = "incomes"
    
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    source = Column(String)
    date = Column(DateTime, default=datetime.utcnow)
    category_id = Column(Integer, ForeignKey("categories.id"))  # Updated to use unified categories table
    wallet_id = Column(Integer, ForeignKey("wallets.id"))
    
    # Relaciones actualizadas
    category = relationship("CategoryDB", back_populates="incomes")
    wallet = relationship("WalletDB", back_populates="incomes")

class IncomeBase(BaseModel):
    amount: float
    source: str
    date: datetime
    category_id: int
    wallet_id: int

    model_config = ConfigDict(from_attributes=True)

class Income(IncomeBase):
    id: int