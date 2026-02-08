from models import Customer, CustomerCreate
from db import SessionDep 
from fastapi import APIRouter, HTTPException, status
from sqlmodel import select



router = APIRouter()




# create customer

@router.post("/customers", response_model=Customer, tags=["customers"])
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)

    return customer




# Get customer list

@router.get("/customers", response_model=list[Customer], tags=["customers"])
async def list_customer(session: SessionDep):
    return session.exec(select(Customer)).all()
   
# Get customer by ID
    
@router.get("/customers/{customer_id}", response_model=Customer , tags=["customers"])
async def get_customer(customer_id: int, session: SessionDep):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer


# Delete customer by ID


@router.delete("/customers/{customer_id}" , tags=["customers"])
async def delete_customer(customer_id: int, session: SessionDep):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    session.delete(customer)
    session.commit()
    return {"message": "Customer deleted successfully"}

# Update customer by ID
@router.put("/customers/{customer_id}", response_model=Customer, tags=["customers"])
async def update_customer(customer_id: int, customer_data: Customer, session: SessionDep):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    customer_data_dict = customer_data.model_dump(exclude_unset=True)
    for key, value in customer_data_dict.items():
        setattr(customer, key, value)
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer