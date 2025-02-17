from fastapi import APIRouter, Depends
from typing import List
from app.models import Category
from app.controllers import get_all_categories
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter( tags=["Categorias"])

@router.get("/categories/", response_model=List[Category])
async def list_categories(db: Session = Depends(get_db)):
    return get_all_categories(db)
