from typing import List, Optional
from sqlalchemy.orm import Session
from ..models import ExpenseDB, CategoryDB, ExpenseCreate, Expense, UserDB , ExpenseType
from .wallet_controller import get_or_create_wallet  # Direct import


def create_expense(db: Session, expense: ExpenseCreate, user_id: int) -> Expense:
    # Get user's wallet
    wallet = get_or_create_wallet(db, user_id)
    
    db_expense = ExpenseDB(
        description=expense.description,
        amount=expense.amount,
        date=expense.date,
        category_id=expense.category_id,  # Cambiado para usar directamente el ID
        wallet_id=wallet.id,
        expense_type=expense.expense_type,
        payment_frequency=expense.payment_frequency,
        installments_number=expense.installments_number,
        current_installment=1 if expense.expense_type == ExpenseType.INSTALLMENT else None
    )
    
    # If it's a fixed or installment expense, update wallet totals
    if expense.expense_type in [ExpenseType.FIXED, ExpenseType.INSTALLMENT]:
        wallet.fixed_expense_total += expense.amount
        if expense.expense_type == ExpenseType.INSTALLMENT and expense.installments_number:
            wallet.monthly_installments += expense.amount / expense.installments_number
    
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

def get_expense(db: Session, expense_id: int) -> Optional[Expense]:
    db_expense = db.query(ExpenseDB).filter(ExpenseDB.id == expense_id).first()
    return Expense.model_validate(db_expense) if db_expense else None

# def get_all_expenses(db: Session, user_id: int) -> List[Expense]:
#     db_expenses = db.query(ExpenseDB).filter(ExpenseDB.user_id == user_id).all()
#     return [Expense.model_validate(exp) for exp in db_expenses]

def get_all_expenses(db: Session, user_id: int) -> List[Expense]:
    # Filtrar gastos mediante el usuario asociado a la wallet
    db_expenses = (
        db.query(ExpenseDB)
          .join(ExpenseDB.wallet)
          .filter(ExpenseDB.wallet.has(user_id=user_id))
          .all()
    )
    return [Expense.model_validate(exp) for exp in db_expenses]


def update_expense(db: Session, expense_id: int, expense_update: ExpenseCreate) -> Optional[Expense]:
    db_expense = db.query(ExpenseDB).filter(ExpenseDB.id == expense_id).first()
    if not db_expense:
        return None
        
    # Get wallet for calculations
    wallet = db_expense.wallet
    
    # If changing from/to installment/fixed, update wallet totals
    if db_expense.expense_type.is_(expense_update.expense_type) is False:
        if db_expense.expense_type in [ExpenseType.FIXED, ExpenseType.INSTALLMENT]:
            wallet.fixed_expense_total -= db_expense.amount
            if db_expense.expense_type == ExpenseType.INSTALLMENT:
                wallet.monthly_installments -= db_expense.amount / db_expense.installments_number
                
        if expense_update.expense_type in [ExpenseType.FIXED, ExpenseType.INSTALLMENT]:
            wallet.fixed_expense_total += expense_update.amount
            if expense_update.expense_type == ExpenseType.INSTALLMENT and expense_update.installments_number:
                wallet.monthly_installments += expense_update.amount / expense_update.installments_number
    
    # Update expense fields
    for key, value in expense_update.dict(exclude={'id'}).items():
        setattr(db_expense, key, value)
    
    db.commit()
    db.refresh(db_expense)
    return db_expense

def delete_expense(db: Session, expense_id: int) -> Optional[Expense]:
    db_expense = db.query(ExpenseDB).filter(ExpenseDB.id == expense_id).first()
    if db_expense:
        expense = Expense.model_validate(db_expense)
        db.delete(db_expense)
        db.commit()
        return expense
    return None



