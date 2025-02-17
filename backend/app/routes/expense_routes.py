from app.controllers.expense_controller import create_expense, delete_expense, update_expense
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models import Expense, ExpenseCreate
from app.controllers import get_all_expenses  # import all functions
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix='/expenses', tags=["Gastos"])

@router.get("/", response_model=List[Expense])
async def list_expenses(db: Session = Depends(get_db)):
    return get_all_expenses(db=db)

@router.post("/", response_model=Expense)
async def add_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    return create_expense(db=db, expense=expense)

@router.put("/{expense_id}/", response_model=Expense)
async def modify_expense(expense_id: int, expense: Expense, db: Session = Depends(get_db)):
    updated = update_expense(db=db, expense_id=expense_id, expense=expense)
    if not updated:
        raise HTTPException(status_code=404, detail="Expense not found")
    return updated

@router.delete("/{expense_id}/", response_model=Expense)
async def remove_expense(expense_id: int, db: Session = Depends(get_db)):
    deleted = delete_expense(db=db, expense_id=expense_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Expense not found")
    return deleted