# backend/app/routes/shared_expense_routes.py
from fastapi import APIRouter, HTTPException, Depends
from app.security import get_current_user
from typing import List
from sqlalchemy.orm import Session
from app.models import SharedExpense, SharedExpenseCreate, UserDB, SharedExpenseStatus , ExpenseDB , SharedExpenseDB
from app.database import get_db
from datetime import datetime

router = APIRouter(prefix='/shared-expenses', tags=["Gastos Compartidos"])

@router.get("/", response_model=List[SharedExpense])
async def list_shared_expenses(
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """Obtener todos los gastos compartidos del usuario actual"""
    return db.query(SharedExpense).filter(SharedExpense.user_id == current_user.id).all()

@router.post("/", response_model=SharedExpense)
async def create_shared_expense(
    shared_expense: SharedExpenseCreate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """Crear un nuevo gasto compartido"""
    db_shared_expense = SharedExpenseDB(**shared_expense.dict())
    db.add(db_shared_expense)
    db.commit()
    db.refresh(db_shared_expense)
    return db_shared_expense

@router.put("/{shared_expense_id}/status", response_model=SharedExpense)
async def update_shared_expense_status(
    shared_expense_id: int,
    status: SharedExpenseStatus,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """Actualizar el estado de un gasto compartido"""
    shared_expense = db.query(SharedExpenseDB).filter(
        SharedExpenseDB.id == shared_expense_id,
        SharedExpenseDB.user_id == current_user.id
    ).first()
    
    if not shared_expense:
        raise HTTPException(status_code=404, detail="Shared expense not found")
    
    shared_expense.status = status
    shared_expense.resolved_at = datetime.utcnow() if status != SharedExpenseStatus.PENDING else None
    db.commit()
    db.refresh(shared_expense)
    return shared_expense

@router.get("/pending", response_model=List[SharedExpense])
async def list_pending_shared_expenses(
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """Obtener gastos compartidos pendientes"""
    return db.query(SharedExpenseDB).filter(
        SharedExpenseDB.user_id == current_user.id,
        SharedExpenseDB.status == SharedExpenseStatus.PENDING
    ).all()

@router.delete("/{shared_expense_id}")
async def delete_shared_expense(
    shared_expense_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """Eliminar un gasto compartido"""
    shared_expense = db.query(SharedExpenseDB).filter(
        SharedExpenseDB.id == shared_expense_id,
        SharedExpenseDB.user_id == current_user.id
    ).first()
    
    if not shared_expense:
        raise HTTPException(status_code=404, detail="Shared expense not found")
    
    db.delete(shared_expense)
    db.commit()
    return {"message": "Shared expense deleted successfully"}

@router.post("/{expense_id}/share/", response_model=SharedExpense)
async def share_expense(
    expense_id: int,
    user_id: int,
    amount: float,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    from app.models.wallet import WalletDB  # si no está importado aún
    # Verificar que el gasto pertenece al usuario actual usando join con la wallet
    expense = (
        db.query(ExpenseDB)
          .join(ExpenseDB.wallet)
          .filter(
            ExpenseDB.id == expense_id,
            WalletDB.user_id == current_user.id
          )
          .first()
    )
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    shared_expense = SharedExpenseCreate(
        expense_id=expense_id,
        wallet_id=expense.wallet_id,
        amount=amount
    )
    return create_shared_expense(db, shared_expense, current_user.id)