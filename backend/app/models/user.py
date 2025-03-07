from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel , ConfigDict
from datetime import datetime
from typing import Optional
from .base import Base


# Modelo de usuario (SQLAlchemy)
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Mantener solo la relación con wallet
    wallet = relationship("WalletDB", back_populates="user", uselist=False , lazy="joined")
    
    # Propiedad calculada para exponer el id de la wallet
    @property
    def wallet_id(self) -> Optional[int]:
        return self.wallet.id if self.wallet else None

# Esquema de usuario (Pydantic)
class User(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    created_at: Optional[datetime] = None
    wallet_id: Optional[int] = None  # Se llenará a partir de la propiedad en UserDB
    
    model_config = ConfigDict(from_attributes=True)
    

# Para ingreso/registro, puedes definir esquemas adicionales (p.ej., UserCreate)
class UserCreate(BaseModel):
    username: str
    email: str
    password: str