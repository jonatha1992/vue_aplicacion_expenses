from app.models.expense import ExpenseType
from fastapi import APIRouter, HTTPException, Depends
from app.security import get_current_user
from typing import List
from app.models import Expense, ExpenseCreate, UserDB , SharedExpense, SharedExpenseCreate , ExpenseDB
from app.controllers import get_all_expenses ,create_shared_expense ,create_expense, delete_expense, update_expense 
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix='/expenses', tags=["Gastos"])

@router.get("/", response_model=List[Expense])
async def list_expenses(
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    return get_all_expenses(db=db, user_id=current_user.id)

# @router.post("/", response_model=Expense)
# async def add_expense(
#     expense: ExpenseCreate,
#     db: Session = Depends(get_db),
#     current_user: UserDB = Depends(get_current_user)
# ):
#     # Validate installment data
#     if expense.expense_type == ExpenseType.INSTALLMENT:
#         if not expense.payment_frequency:
#             raise HTTPException(
#                 status_code=400, 
#                 detail="Payment frequency required for installment expenses"
#             )
#         if not expense.installments_number:
#             raise HTTPException(
#                 status_code=400,
#                 detail="Number of installments required"
#             )
    
#     return create_expense(db=db, expense=expense, user_id=current_user.id)

@router.post("/", response_model=Expense)
async def add_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    return create_expense(db=db, expense=expense, user_id=current_user.id)
@router.put("/{expense_id}/", response_model=Expense)
async def modify_expense(
    expense_id: int,
    expense_update: ExpenseCreate,  # Changed from expense: Expense
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    updated = update_expense(db=db, expense_id=expense_id, expense_update=expense_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Expense not found")
    return updated

@router.delete("/{expense_id}/")
async def remove_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    try:
        deleted = delete_expense(db=db, expense_id=expense_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Expense not found")
        return {"message": "Expense deleted successfully", "id": expense_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{expense_id}/share/", response_model=SharedExpense)
async def share_expense(
    expense_id: int,
    user_id: int,
    amount: float,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    # Verificar que el gasto pertenece al usuario actual
    expense = db.query(ExpenseDB).filter(
        ExpenseDB.id == expense_id,
        ExpenseDB.user_id == current_user.id
    ).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    shared_expense = SharedExpenseCreate(
        expense_id=expense_id,
        wallet_id=expense.wallet_id,
        amount=amount
    )
    return create_shared_expense(db, shared_expense, current_user.id)