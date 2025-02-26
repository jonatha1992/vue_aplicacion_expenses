from app.controllers import get_user_by_username, create_user, get_all_user, get_user_by_email
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import UserCreate, User
from app.security import get_password_hash, verify_password, create_access_token
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/register", response_model=User)
async def register(user_create: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_username(db, user_create.username)
    existing_email = get_user_by_email(db, user_create.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = get_password_hash(user_create.password)
    user_create.password = hashed_pw
    new_user = create_user(db, user_create)
    return new_user

@router.post("/login")
async def login(form_data: UserCreate, db: Session = Depends(get_db)):
    user = get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username,
        "user_id": user.id
    }

# Ruta renombrada para evitar conflicto con POST /login
@router.get("/users")
async def list_user(db: Session = Depends(get_db)):
    return get_all_user(db)