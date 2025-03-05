from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime
from typing import Optional
from .base import Base

from enum import Enum as PyEnum

class ExpenseType(str, PyEnum):
    SINGLE = 'único'
    INSTALLMENT = 'cuota'
    FIXED = 'fijo'

class PaymentFrequency(str, PyEnum):
    WEEKLY = 'semanal'
    MONTHLY = 'mensual'
    QUARTERLY = 'trimestral'
    BIANNUAL = 'semestral'
    ANNUAL = 'anual'


class ExpenseDB(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    category_id = Column(Integer, ForeignKey("categories.id"))
    wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=False)
    
    # Modified/New fields
    expense_type = Column(Enum(ExpenseType), default=ExpenseType.SINGLE)
    payment_frequency = Column(Enum(PaymentFrequency), nullable=True)
    installments_number = Column(Integer, nullable=True)  # Número total de cuotas
    current_installment = Column(Integer, nullable=True)  # Cuota actual
    
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.utcnow(), onupdate=lambda: datetime.utcnow())
    
    wallet = relationship("WalletDB", back_populates="expenses")
    category = relationship("CategoryDB", back_populates="expenses")
    shared_expenses = relationship("SharedExpenseDB", back_populates="expense", cascade="all, delete-orphan")

    @property
    def user(self):
        """Obtener usuario a través de wallet"""
        return self.wallet.user

# Pydantic models
class ExpenseCreate(BaseModel):
    description: str
    amount: float
    date: datetime
    category_id: int
    expense_type: ExpenseType = ExpenseType.SINGLE
    payment_frequency: Optional[PaymentFrequency] = None
    installments_number: Optional[int] = None
    current_installment: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator('installments_number')
    @classmethod
    def validate_installments(cls, v: Optional[int], info) -> Optional[int]:
        if info.data.get('expense_type') == ExpenseType.INSTALLMENT and not v:
            raise ValueError('Number of installments is required for installment expenses')
        if v is not None and v <= 0:
            raise ValueError('Number of installments must be greater than 0')
        return v

    @field_validator('payment_frequency')
    @classmethod
    def validate_payment_frequency(cls, v: Optional[PaymentFrequency], info) -> Optional[PaymentFrequency]:
        if info.data.get('expense_type') == ExpenseType.INSTALLMENT and not v:
            raise ValueError('Payment frequency is required for installment expenses')
        return v

    @field_validator('expense_type')
    @classmethod
    def validate_expense_type(cls, v: ExpenseType, info) -> ExpenseType:
        if v == ExpenseType.INSTALLMENT:
            if not info.data.get('payment_frequency'):
                raise ValueError('Payment frequency required for installment expenses')
            if not info.data.get('installments_number'):
                raise ValueError('Number of installments required for installment expenses')
        return v

class Expense(ExpenseCreate):
    id: int