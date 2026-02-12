from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship 
from typing import List, Optional

# --- Plan Models ---

class CustomerPlan(SQLModel, table=True):
    # Added | None = Field(default=None...) to ensure the DB generates the ID properly
    id: int | None = Field(default=None, primary_key=True)
    plan_id: int = Field(foreign_key="plan.id")
    customer_id: int = Field(foreign_key="customer.id")

class Plan(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(default=None)
    price: int = Field(default=None)
    description: str = Field(default=None)
    # Relationship to Customer via CustomerPlan
    customers: list["Customer"] = Relationship(back_populates="plans", link_model=CustomerPlan)

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
    transactions: List["Transaction"] = Relationship(back_populates="customer")
    invoices: List["Invoice"] = Relationship(back_populates="customer")
    plans: list["Plan"] = Relationship(back_populates="customers", link_model=CustomerPlan)

# --- Response Models (The Firewalls) ---

class CustomerRead(CustomerBase):
    id: int

class CustomerPlanRead(SQLModel):
    id: int
    customer_id: int
    plan_id: int

# --- 2. TRANSACTION & INVOICE MODELS ---

class TransactionBase(SQLModel):
    amount: int
    description: str
    customer_id: int = Field(foreign_key="customer.id")

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customer: Optional["Customer"] = Relationship(back_populates="transactions")
    invoice_id: int | None = Field(default=None, foreign_key="invoice.id")
    invoice: Optional["Invoice"] = Relationship(back_populates="transactions")

class Invoice(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")
    transactions: List["Transaction"] = Relationship(back_populates="invoice")
    customer: Optional["Customer"] = Relationship(back_populates="invoices")

    @property
    def total_price(self) -> int:
        return sum(t.amount for t in self.transactions)