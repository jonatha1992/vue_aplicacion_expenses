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
    user_id = Column(Integer, ForeignKey("users.id"))  # Nuevo campo para referenciar al usuario
    category_rel = relationship("CategoryDB", back_populates="expenses")
    user = relationship("UserDB", back_populates="expenses")  # Relación inversa con usuario

# Pydantic models


class ExpenseCreate(BaseModel):
    description: str
    amount: float
    date: datetime
    category_id: int  # se envía el id de la categoría
    # Puedes agregar opcionalmente user_id aquí si lo deseas

    class Config:
        from_attributes = True

class Expense(ExpenseCreate):
    id: Optional[int] = None
