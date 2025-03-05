# backend/app/models/shared_expense.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional
import enum
from .base import Base

# Enum para el estado del gasto compartido
class SharedExpenseStatus(str, enum.Enum):
    PENDING = "pendiente"
    ACCEPTED = "aceptado"	
    REJECTED = "rechazado"

# Modelo SQLAlchemy
class SharedExpenseDB(Base):
    __tablename__ = "shared_expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    expense_id = Column(Integer, ForeignKey("expenses.id"))
    amount = Column(Float)
    status = Column(String, default=SharedExpenseStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)  # Se actualiza automáticamente
    resolved_at = Column(DateTime, nullable=True)  # Para cuando se acepta o rechaza
    # Relaciones
    user = relationship("UserDB", back_populates="shared_expenses")
    expense = relationship("ExpenseDB", back_populates="shared_expenses")

# Modelos Pydantic
class SharedExpenseBase(BaseModel):
    user_id: int
    expense_id: int
    amount: float = Field(gt=0)
    status: SharedExpenseStatus = SharedExpenseStatus.PENDING
    updated_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None


    model_config = ConfigDict(from_attributes=True)

class SharedExpenseCreate(SharedExpenseBase):
    pass

class SharedExpense(SharedExpenseBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True