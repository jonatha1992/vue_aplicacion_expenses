from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.models import Income, UserDB, IncomeBase  # Agregar IncomeBase
from app.controllers import (
    create_income,
    get_incomes_by_wallet,
    get_income_by_id,
    delete_income,
    update_income,
)
from app.database import get_db
from app.security import get_current_user
from app.controllers.wallet_controller import get_or_create_wallet

router = APIRouter(prefix="/incomes", tags=["Ingresos"])

@router.get("/", response_model=List[Income])
async def list_incomes(
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """Obtener todos los ingresos del usuario actual"""
    wallet = get_or_create_wallet(db, current_user.id)
    return get_incomes_by_wallet(db, wallet.id)

@router.post("/", response_model=Income)
async def add_income(
    income_data: dict,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """Crear un nuevo ingreso"""
    wallet = get_or_create_wallet(db, current_user.id)
    return create_income(db, income_data, wallet.id)

@router.get("/{income_id}", response_model=Income)
async def get_income(
    income_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """Obtener un ingreso específico"""
    income = get_income_by_id(db, income_id)
    if not income:
        raise HTTPException(status_code=404, detail="Income not found")
    if income.wallet.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this income")
    return income

@router.put("/{income_id}", response_model=Income)
async def update_income_route(
    income_id: int,
    income_data: dict,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """Actualizar un ingreso existente"""
    existing_income = get_income_by_id(db, income_id)
    if not existing_income:
        raise HTTPException(status_code=404, detail="Income not found")
    if existing_income.wallet.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this income")
    
    updated_income = update_income(db, income_id, income_data)
    if not updated_income:
        raise HTTPException(status_code=400, detail="Error updating income")
    return updated_income

@router.delete("/{income_id}")
async def remove_income(
    income_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """Eliminar un ingreso"""
    existing_income = get_income_by_id(db, income_id)
    if not existing_income:
        raise HTTPException(status_code=404, detail="Income not found")
    if existing_income.wallet.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this income")
    
    if delete_income(db, income_id):
        return {"message": "Income deleted successfully"}
    raise HTTPException(status_code=400, detail="Error deleting income")
