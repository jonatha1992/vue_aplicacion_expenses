from typing import List, Optional
from sqlalchemy.orm import Session
from ..models import  CategoryDB

def get_all_categories(db: Session) -> List[CategoryDB]:
    return db.query(CategoryDB).all()

