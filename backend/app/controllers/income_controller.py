from typing import List, Optional
from sqlalchemy.orm import Session
from ..models import IncomeDB, WalletDB
from datetime import datetime

def create_income(db: Session, income_data: dict, wallet_id: int) -> IncomeDB:
    new_income = IncomeDB(
        amount=income_data["amount"],
        source=income_data["source"],
        date=income_data.get("date", datetime.utcnow()),
        category_id=income_data["category_id"],
        wallet_id=wallet_id
    )
    db.add(new_income)
    db.commit()
    db.refresh(new_income)
    
    # Actualizar el balance de la wallet
    wallet = db.query(WalletDB).filter(WalletDB.id == wallet_id).first()
    if wallet:
        wallet.total_income += new_income.amount
        wallet.balance += new_income.amount
        db.commit()
    
    return new_income

def get_incomes_by_wallet(db: Session, wallet_id: int) -> List[IncomeDB]:
    return db.query(IncomeDB).filter(IncomeDB.wallet_id == wallet_id).all()

def get_income_by_id(db: Session, income_id: int) -> Optional[IncomeDB]:
    return db.query(IncomeDB).filter(IncomeDB.id == income_id).first()

def delete_income(db: Session, income_id: int) -> bool:
    income = get_income_by_id(db, income_id)
    if income:
        # Actualizar el balance de la wallet
        wallet = db.query(WalletDB).filter(WalletDB.id == income.wallet_id).first()
        if wallet:
            wallet.total_income -= income.amount
            wallet.balance -= income.amount
            
        db.delete(income)
        db.commit()
        return True
    return False

def update_income(db: Session, income_id: int, income_data: dict) -> Optional[IncomeDB]:
    income = get_income_by_id(db, income_id)
    if income:
        old_amount = income.amount
        
        # Actualizar campos
        for key, value in income_data.items():
            setattr(income, key, value)
            
        db.commit()
        db.refresh(income)
        
        # Actualizar el balance de la wallet
        wallet = db.query(WalletDB).filter(WalletDB.id == income.wallet_id).first()
        if wallet:
            wallet.total_income = wallet.total_income - old_amount + income.amount
            wallet.balance = wallet.balance - old_amount + income.amount
            db.commit()
            
        return income
    return None