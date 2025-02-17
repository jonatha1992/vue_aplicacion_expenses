from typing import List, Optional
from sqlalchemy.orm import Session
from ..models import  UserDB
from app.models import User  # ensure the User model is imported


def get_user_by_username(db:Session , username: str):
    return db.query(UserDB).filter(UserDB.username == username).first()

def get_user_by_email(db:Session , email: str):
    return db.query(UserDB).filter(UserDB.email == email).first()

def create_user(db: Session, user_create):
    # Optionally: encode password here if needed, already hashed in user_create.password
    new_user = UserDB(
        username=user_create.username,
        email=user_create.email,           # added email field
        hashed_password=user_create.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all_user(db: Session)-> List[UserDB]:
    return db.query(UserDB).all()
