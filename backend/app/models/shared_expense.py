# backend/app/models/shared_expense.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, CheckConstraint
from sqlalchemy.orm import relationship
from pydantic import BaseModel, ConfigDict, Field, validator
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
    """
    Modelo para gastos compartidos entre wallets.
    
    Attributes:
        wallet_id: ID de la wallet con quien se comparte el gasto
        expense_id: ID del gasto compartido
        amount: Monto compartido
        status: Estado del gasto compartido
    """
    __tablename__ = "shared_expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(Integer, ForeignKey("wallets.id"), index=True)  # Cambiado de user_id a wallet_id
    expense_id = Column(Integer, ForeignKey("expenses.id"), index=True)
    amount = Column(Float, CheckConstraint('amount > 0'))
    status = Column(Enum(SharedExpenseStatus), default=SharedExpenseStatus.PENDING, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    __table_args__ = (
        CheckConstraint('amount > 0', name='check_positive_amount'),
    )

    # Relaciones actualizadas
    wallet = relationship("WalletDB", back_populates="shared_expenses")  # Nueva relación con wallet
    expense = relationship("ExpenseDB", back_populates="shared_expenses")

# Modelos Pydantic
class SharedExpenseBase(BaseModel):
    wallet_id: int  # Cambiado de user_id a wallet_id
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