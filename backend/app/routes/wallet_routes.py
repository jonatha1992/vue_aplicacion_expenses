from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models import Wallet
from app.controllers import get_or_create_wallet, calculate_totals ,calculate_monthly_expenses, get_expense_distribution, get_balance_history
from app.database import get_db
from app.security import get_current_user
from sqlalchemy.orm import Session

router = APIRouter(prefix="/wallet", tags=["Wallet"])

@router.get("/", response_model=Wallet)
async def get_wallet(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene o crea la wallet del usuario actual"""
    return get_or_create_wallet(db, current_user.id)

@router.get("/balance")
async def get_balance(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene el balance actual y totales de la wallet"""
    wallet = get_or_create_wallet(db, current_user.id)
    return calculate_totals(db, wallet.id)

@router.get("/statistics")
async def get_statistics(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene estadísticas de gastos e ingresos"""
    wallet = get_or_create_wallet(db, current_user.id)
    return {
        "monthly_expenses": calculate_monthly_expenses(db, wallet.id),
        "category_distribution": get_expense_distribution(db, wallet.id),
        "balance_history": get_balance_history(db, wallet.id)
    }