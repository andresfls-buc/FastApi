from models import TransactionCreate, Transaction
from db import SessionDep
from fastapi import APIRouter
from sqlmodel import select

router = APIRouter()


# Create transaction and invoice

@router.post("/transactions" , tags=["Transactions"])
async def create_transaction(transaction_data: TransactionCreate, session: SessionDep):
    transaction = Transaction.model_validate(transaction_data.model_dump())
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction

# Get transaction list
@router.get("/transactions", response_model=list[Transaction], tags=["Transactions"])
async def list_transaction(session: SessionDep):
    return session.exec(select(Transaction)).all()