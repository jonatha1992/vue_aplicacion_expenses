from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models import Expense, ExpenseCreate
from app.controllers import crud
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/expenses/", response_model=List[Expense])
async def list_expenses(db: Session = Depends(get_db)):
    return crud.get_all_expenses(db=db)

@router.post("/expenses/", response_model=Expense)
async def add_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    return crud.create_expense(db=db, expense=expense)

@router.put("/expenses/{expense_id}/", response_model=Expense)
async def modify_expense(expense_id: int, expense: Expense, db: Session = Depends(get_db)):
    updated = crud.update_expense(db=db, expense_id=expense_id, expense=expense)
    if not updated:
        raise HTTPException(status_code=404, detail="Expense not found")
    return updated

@router.delete("/expenses/{expense_id}/", response_model=Expense)
async def remove_expense(expense_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_expense(db=db, expense_id=expense_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Expense not found")
    return deleted