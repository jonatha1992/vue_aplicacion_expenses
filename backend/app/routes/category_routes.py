from fastapi import APIRouter, Depends
from typing import List, Optional
from app.models import Category, CategoryType
from app.controllers import get_all_categories
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/categories", tags=["Categorias"])

@router.get("/", response_model=List[Category])
async def list_categories(
    type: Optional[CategoryType] = None,
    db: Session = Depends(get_db)
):
    return get_all_categories(db, type)

@router.get("/expenses", response_model=List[Category])
async def list_expense_categories(db: Session = Depends(get_db)):
    return get_all_categories(db, CategoryType.EXPENSE)

@router.get("/incomes", response_model=List[Category])
async def list_income_categories(db: Session = Depends(get_db)):
    return get_all_categories(db, CategoryType.INCOME)
