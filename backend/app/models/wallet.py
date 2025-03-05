from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, ConfigDict
from .base import Base

class WalletDB(Base):
    __tablename__ = "wallets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    balance = Column(Float, default=0)
    total_income = Column(Float, default=0)
    total_expense = Column(Float, default=0)
    monthly_installments = Column(Float, default=0)
    fixed_expense_total = Column(Float, default=0)

    # Relación única con usuario
    user = relationship("UserDB", back_populates="wallet", uselist=False)
    # Relaciones uno a muchos
    expenses = relationship("ExpenseDB", back_populates="wallet", cascade="all, delete-orphan")
    incomes = relationship("IncomeDB", back_populates="wallet", cascade="all, delete-orphan")

class WalletBase(BaseModel):
    balance: float
    total_income: float
    total_expense: float
    monthly_installments: float
    fixed_expense_total: float

    model_config = ConfigDict(from_attributes=True)


class Wallet(WalletBase):
    id: int
    user_id: int