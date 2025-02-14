from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models import Expense
from app import crud
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/expenses", tags=["expenses"])

@router.get("/", response_model=list[Expense])  # Changed List to list
def list_expenses(db: Session = Depends(get_db)):
    return crud.get_all_expenses(db=db)

@router.post("/", response_model=Expense)
def add_expense(expense: Expense, db: Session = Depends(get_db)):
    return crud.create_expense(db=db, expense=expense)

@router.put("/{expense_id}", response_model=Expense)
def modify_expense(expense_id: int, expense: Expense, db: Session = Depends(get_db)):
    updated = crud.update_expense(db=db, expense_id=expense_id, expense=expense)
    if not updated:
        raise HTTPException(status_code=404, detail="Expense not found")
    return updated

@router.delete("/{expense_id}", response_model=Expense)
def remove_expense(expense_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_expense(db=db, expense_id=expense_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Expense not found")
    return deleted