from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship 
from typing import List, Optional

# --- 1. CUSTOMER MODELS ---

class CustomerBase(SQLModel):
    name: str = Field(default=None)
    description: str | None = Field(default=None)
    email: EmailStr = Field(default=None)
    age: int = Field(default=None, ge=0, le=120)

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # Correct: Points to Transaction.customer and Invoice.customer
    transactions: List["Transaction"] = Relationship(back_populates="customer")
    invoices: List["Invoice"] = Relationship(back_populates="customer")


# --- 2. TRANSACTION & INVOICE MODELS ---

class TransactionBase(SQLModel):
    amount: int
    description: str
    customer_id: int = Field(foreign_key="customer.id")

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    
    # Handshake with Customer.transactions
    customer: Optional["Customer"] = Relationship(back_populates="transactions")
    
    # Links to the ID in the DB
    invoice_id: int | None = Field(default=None, foreign_key="invoice.id")
    # Handshake with Invoice.transactions
    invoice: Optional["Invoice"] = Relationship(back_populates="transactions")


class Invoice(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")

    # Handshake with Transaction.invoice
    transactions: List["Transaction"] = Relationship(back_populates="invoice")
    
    # Handshake with Customer.invoices
    customer: Optional["Customer"] = Relationship(back_populates="invoices")

    @property
    def total_price(self) -> int:
        # This works because of the Relationship above
        return sum(t.amount for t in self.transactions)