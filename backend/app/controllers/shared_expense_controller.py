from typing import List, Optional
from sqlalchemy.orm import Session
from ..models import SharedExpenseDB, SharedExpenseCreate, SharedExpense, ExpenseDB
from fastapi import HTTPException

def verify_expense_ownership(db: Session, expense_id: int, user_id: int):
    expense = db.query(ExpenseDB).filter(
        ExpenseDB.id == expense_id,
        ExpenseDB.user_id == user_id
    ).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

def create_shared_expense(db: Session, shared_expense: SharedExpenseCreate, owner_id: int) -> SharedExpense:
    # Verificar propiedad del gasto
    expense = verify_expense_ownership(db, shared_expense.expense_id, owner_id)
    
    # Verificar que el monto compartido no exceda el original
    if float(shared_expense.amount) > float(expense.amount):
        raise HTTPException(status_code=400, detail="Shared amount cannot exceed original expense amount")
    
    # Verificar que no exista un gasto compartido previo
    existing_share = db.query(SharedExpenseDB).filter(
        SharedExpenseDB.expense_id == shared_expense.expense_id,
        SharedExpenseDB.user_id == shared_expense.user_id
    ).first()
    
    if existing_share:
        raise HTTPException(status_code=400, detail="Expense already shared with this user")
    
    db_shared_expense = SharedExpenseDB(**shared_expense.dict())
    db.add(db_shared_expense)
    db.commit()
    db.refresh(db_shared_expense)
    return db_shared_expense

def get_shared_expenses(db: Session, user_id: int) -> List[SharedExpenseDB]:
    return db.query(SharedExpenseDB).filter(
        SharedExpenseDB.user_id == user_id
    ).all()

def update_shared_expense_status(
    db: Session, 
    shared_expense_id: int, 
    status: str,
    user_id: int
    ) -> SharedExpense:
    shared_expense = db.query(SharedExpenseDB).filter(
        SharedExpenseDB.id == shared_expense_id,
        SharedExpenseDB.user_id == user_id
    ).first()
    
    if not shared_expense:
        raise HTTPException(status_code=404, detail="Shared expense not found")
    
    shared_expense.status = status
    db.commit()
    db.refresh(shared_expense)
    return shared_expense