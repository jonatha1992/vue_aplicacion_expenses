from typing import List, Optional
from sqlalchemy.orm import Session
from ..models import ExpenseDB, CategoryDB, ExpenseCreate, Expense , UserDB
from app.models import User  # ensure the User model is imported

def create_expense(db: Session, expense: ExpenseCreate) -> Expense:
    # Create expense
    db_expense = ExpenseDB(
        description=expense.description,
        amount=expense.amount,
        date=expense.date,
        category_id=expense.category_id  # Cambiado para usar directamente el ID
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    
    # Convert to Pydantic model
    return Expense.model_validate(db_expense)

def get_expense(db: Session, expense_id: int) -> Optional[Expense]:
    db_expense = db.query(ExpenseDB).filter(ExpenseDB.id == expense_id).first()
    return Expense.model_validate(db_expense) if db_expense else None

def get_all_expenses(db: Session) -> List[Expense]:
    db_expenses = db.query(ExpenseDB).all()
    return [Expense.model_validate(exp) for exp in db_expenses]

def update_expense(db: Session, expense_id: int, expense: Expense) -> Optional[Expense]:
    db_expense = db.query(ExpenseDB).filter(ExpenseDB.id == expense_id).first()
    if db_expense:
        for key, value in expense.model_dump(exclude={'id'}).items():
            setattr(db_expense, key, value)
        db.commit()
        db.refresh(db_expense)
        return Expense.model_validate(db_expense)
    return None

def delete_expense(db: Session, expense_id: int) -> Optional[Expense]:
    db_expense = db.query(ExpenseDB).filter(ExpenseDB.id == expense_id).first()
    if db_expense:
        expense = Expense.model_validate(db_expense)
        db.delete(db_expense)
        db.commit()
        return expense
    return None

def get_all_categories(db: Session) -> List[CategoryDB]:
    return db.query(CategoryDB).all()

def get_user_by_username(db:Session , username: str):
    return db.query(UserDB).filter(UserDB.username == username).first()

def create_user(db: Session, user_create):
    # Optionally: encode password here if needed, already hashed in user_create.password
    new_user = UserDB(
        username=user_create.username,
        email=user_create.email,           # added email field
        hashed_password=user_create.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all_user(db: Session)-> List[UserDB]:
    return db.query(UserDB).all()
