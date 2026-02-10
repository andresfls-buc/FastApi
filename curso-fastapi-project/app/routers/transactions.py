from models import Customer, TransactionCreate, Transaction
from db import SessionDep
from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

router = APIRouter()


# Create transaction and invoice

@router.post("/transactions" , status_code= status.HTTP_201_CREATED , tags=["Transactions"])
async def create_transaction(transaction_data: TransactionCreate, session: SessionDep):
    customer = session.get(Customer, transaction_data.customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    
    transaction_db = Transaction.model_validate(transaction_data)
    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)
    return transaction_db

# Get transaction list
@router.get("/transactions", response_model=list[Transaction], tags=["Transactions"])
async def list_transaction(session: SessionDep):
    query = select(Transaction)
    transactions = session.exec(query).all()
    return transactions