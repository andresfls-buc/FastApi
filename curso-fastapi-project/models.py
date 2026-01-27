from pydantic import BaseModel , EmailStr


class Customer(BaseModel):
    name: str
    description: str | None
    # Using EmailStr for email validation
    email: EmailStr           
    age: int


#Transaction model

class Transaction(BaseModel):
    id: int
    amount: int
    description: str
   

# Invoice model including Customer and list of Transactions
class Invoice(BaseModel):
    id: int
    customer: Customer
    transactions: list[Transaction]
    total: int

    @property
    def total(self):
        return sum(transaction.amount for transaction in self.transactions)