from typing import Optional, Dict, List
from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from ..models import WalletDB, ExpenseDB, CategoryDB
from calendar import monthrange

def get_or_create_wallet(db: Session, user_id: int) -> WalletDB:
    wallet = db.query(WalletDB).filter(WalletDB.user_id == user_id).first()
    if not wallet:
        wallet = WalletDB(user_id=user_id)
        db.add(wallet)
        db.commit()
        db.refresh(wallet)
    return wallet

def calculate_totals(db: Session, wallet_id: int):
    wallet = db.query(WalletDB).filter(WalletDB.id == wallet_id).first()
    if wallet:
        # Calcular totales
        expenses = db.query(ExpenseDB).filter(ExpenseDB.wallet_id == wallet_id).all()
        wallet.total_expense = sum(e.amount for e in expenses)
        wallet.balance = wallet.total_income - wallet.total_expense
        db.commit()
    return wallet

def calculate_monthly_expenses(db: Session, wallet_id: int) -> Dict:
    """Calcula los gastos mensuales de los últimos 6 meses"""
    today = datetime.now()
    six_months_ago = today - timedelta(days=180)
    
    expenses = db.query(
        func.sum(ExpenseDB.amount).label('total'),
        func.extract('month', ExpenseDB.date).label('month')
    ).filter(
        ExpenseDB.wallet_id == wallet_id,
        ExpenseDB.date >= six_months_ago
    ).group_by(
        func.extract('month', ExpenseDB.date)
    ).all()
    
    return {
        str(expense.month): float(expense.total) 
        for expense in expenses
    }

def get_expense_distribution(db: Session, wallet_id: int) -> Dict:
    """Obtiene la distribución de gastos por categoría"""
    expenses = db.query(
        func.sum(ExpenseDB.amount).label('total'),
        CategoryDB.name
    ).join(
        CategoryDB
    ).filter(
        ExpenseDB.wallet_id == wallet_id
    ).group_by(
        CategoryDB.name
    ).all()
    
    return {
        expense.name: float(expense.total)
        for expense in expenses
    }

def get_balance_history(db: Session, wallet_id: int) -> List[Dict]:
    """Obtiene el historial de balance diario del último mes"""
    today = datetime.now()
    start_of_month = today.replace(day=1)
    
    daily_expenses = db.query(
        func.sum(ExpenseDB.amount).label('expense_total'),
        func.date(ExpenseDB.date).label('date')
    ).filter(
        ExpenseDB.wallet_id == wallet_id,
        ExpenseDB.date >= start_of_month
    ).group_by(
        func.date(ExpenseDB.date)
    ).all()
    
    # Obtener el balance inicial del mes
    wallet = db.query(WalletDB).filter(WalletDB.id == wallet_id).first()
    if not wallet:
        return []
    current_balance = wallet.balance
    
    balance_history = []
    for day in range(today.day):
        date = start_of_month + timedelta(days=day)
        daily_expense = next(
            (e.expense_total for e in daily_expenses if e.date == date.date()),
            0
        )
        
        balance_history.append({
            "date": date.strftime("%Y-%m-%d"),
            "balance": current_balance - daily_expense
        })
        current_balance -= daily_expense
    
    return balance_history