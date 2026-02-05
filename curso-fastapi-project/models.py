from pydantic import EmailStr
from sqlmodel import SQLModel, Field
from typing import List, Optional

# --- 1. CUSTOMER MODELS (The DTO Pattern) ---

class CustomerBase(SQLModel):
    """
    Shared fields. Both the DB and the API will use these.
    """
    name: str
    description: Optional[str] = None
    email: EmailStr
    age: int

class CustomerCreate(CustomerBase):
    """
    Used when creating a customer. 
    The user doesn't send an ID; the DB generates it.
    """
    pass

class Customer(CustomerBase, table=True):
    """
    The actual SQLite Table.
    Includes the ID which is the Primary Key.
    """
    id: Optional[int] = Field(default=None, primary_key=True)


# --- 2. TRANSACTION & INVOICE MODELS ---

class Transaction(SQLModel):
    """
    Simple model for transactions. 
    If you want this in the DB later, add 'table=True'.
    """
    id: int
    amount: int
    description: str


class Invoice(SQLModel):
    id: int
    customer: Customer # This nests the Customer object inside the Invoice
    transactions: List[Transaction]

    @property
    def total_price(self) -> int:
        """Calculates total on the fly without storing it in the DB."""
        return sum(t.amount for t in self.transactions)