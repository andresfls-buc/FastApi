from pydantic import EmailStr
from sqlmodel import SQLModel, Field
from typing import List, Optional

# --- 1. CUSTOMER MODELS ---

class CustomerBase(SQLModel):
    name: str = Field(default=None)
    description: str | None = Field(default=None)
    email: EmailStr = Field(default=None)
    age: int = Field(default=None, ge=0, le=120)

class CustomerCreate(CustomerBase):
    # This remains empty because it only needs what's in CustomerBase
    pass

class Customer(CustomerBase, table=True):
    # primary_key=True tells the DB to handle auto-incrementing
    # The 'None' default allows the DB to generate the value without Python complaining
    id: int | None = Field(default=None, primary_key=True)


# --- 2. TRANSACTION & INVOICE MODELS ---

class TransactionCreate(SQLModel):
    """Created a 'Create' version so users don't have to guess the Transaction ID either."""
    amount: int
    description: str

class Transaction(TransactionCreate, table=True):
    """The actual DB table for Transactions."""
    id: int | None = Field(default=None, primary_key=True)


class Invoice(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    
    # FIX: Use 'CustomerCreate' instead of 'Customer' 
    # This removes the 'id' requirement from the POST request body
    customer: CustomerCreate 
    
    # FIX: Use 'TransactionCreate' for the same reason
    transactions: List[TransactionCreate]

    @property
    def total_price(self) -> int:
        return sum(t.amount for t in self.transactions)