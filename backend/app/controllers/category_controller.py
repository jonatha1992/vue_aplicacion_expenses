from typing import List
from sqlalchemy.orm import Session
from ..models import CategoryDB, CategoryType

def get_all_categories(db: Session, type: CategoryType = None) -> List[CategoryDB]:
    query = db.query(CategoryDB)
    if type:
        query = query.filter(CategoryDB.type == type)
    return query.all()



