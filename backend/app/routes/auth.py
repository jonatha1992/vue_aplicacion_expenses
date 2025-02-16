from app.controllers import crud
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app import database
from app.models import UserCreate, User
from app.security import get_password_hash, verify_password, create_access_token  # define estas funciónes
from datetime import timedelta

# router = APIRouter(prefix="/auth", tags=["auth"])
router = APIRouter()

@router.post("/register", response_model=User)
def register(user_create: UserCreate, db: Session = Depends(database.get_db)):
    existing_user = crud.get_user_by_username(db, user_create.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_pw = get_password_hash(user_create.password)
    user_create.password = hashed_pw
    new_user = crud.create_user(db, user_create)
    return new_user

@router.post("/login")
def login(form_data: UserCreate, db: Session = Depends(database.get_db)):
    # Aquí deberías implementar la lógica de autenticación,
    # verificando usuario, password y retornando un token JWT.
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}