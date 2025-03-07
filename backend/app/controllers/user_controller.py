from typing import List, Optional
from sqlalchemy.orm import Session
from ..models import  UserDB , WalletDB , User


def get_user_by_username(db:Session , username: str):
    return db.query(UserDB).filter(UserDB.username == username).first()

def get_user_by_email(db:Session , email: str):
    return db.query(UserDB).filter(UserDB.email == email).first()

def create_user(db: Session, user_create):
    new_user = UserDB(
        username=user_create.username,
        email=user_create.email,           # added email field
        hashed_password=user_create.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Crear wallet automáticamente
    wallet = WalletDB(user_id=new_user.id)
    db.add(wallet)
    db.commit()
    db.refresh(new_user)  # Refrescar nuevamente para cargar la relación
    return new_user


def get_all_user(db: Session)-> List[UserDB]:
    return db.query(UserDB).all()
