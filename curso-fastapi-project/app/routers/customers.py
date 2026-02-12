from models import Customer, CustomerCreate, CustomerPlanRead, Plan, CustomerRead, CustomerPlan 
from db import SessionDep 
from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from typing import List

router = APIRouter()

# CREATE CUSTOMER
@router.post("/customers", response_model=CustomerRead, tags=["customers"])
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

# GET ALL CUSTOMERS
@router.get("/customers", response_model=List[CustomerRead], tags=["customers"])
async def list_customer(session: SessionDep):
    return session.exec(select(Customer)).all()
   
# GET CUSTOMER BY ID
@router.get("/customers/{customer_id}", response_model=CustomerRead, tags=["customers"])
async def get_customer(customer_id: int, session: SessionDep):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer

# SUBSCRIBE CUSTOMER TO PLAN (FIXED TO SHOW IDs)

@router.post("/customers/{customer_id}/plans/{plan_id}", response_model=CustomerPlanRead, tags=["customers"])
async def subscribe_customer_to_plan(customer_id: int, plan_id: int, session: SessionDep):
    # 1. Check existence
    customer = session.get(Customer, customer_id)
    plan = session.get(Plan, plan_id)

    if not customer or not plan:
        raise HTTPException(status_code=404, detail="Customer or Plan not found")
    
    # 2. Check for existing link (N to N check)
    statement = select(CustomerPlan).where(
        CustomerPlan.customer_id == customer_id, 
        CustomerPlan.plan_id == plan_id
    )
    existing_link = session.exec(statement).first()

    if existing_link:
        raise HTTPException(status_code=400, detail="Subscription already exists")

    # 3. Create the link record
    new_link = CustomerPlan(customer_id=customer_id, plan_id=plan_id)
    
    session.add(new_link)
    session.commit()
    
    # 4. Refreshing 'new_link' is what pulls the ID from the database!
    session.refresh(new_link)

    # 5. Return the link object so we see the IDs in the JSON
    return new_link

@router.get("/customers/{customer_id}/plans", response_model=List[Plan], tags=["customers"])
async def subscribe_customer_to_plan(customer_id: int, session: SessionDep):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer.plans

# DELETE CUSTOMER
@router.delete("/customers/{customer_id}", tags=["customers"])
async def delete_customer(customer_id: int, session: SessionDep):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    session.delete(customer)
    session.commit()
    return {"message": "Customer deleted successfully"}

# UPDATE CUSTOMER
@router.put("/customers/{customer_id}", response_model=CustomerRead, tags=["customers"])
async def update_customer(customer_id: int, customer_data: CustomerCreate, session: SessionDep):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    update_data = customer_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(customer, key, value)
        
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer