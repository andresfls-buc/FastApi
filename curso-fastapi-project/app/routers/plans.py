from fastapi import APIRouter ,status , HTTPException
from sqlmodel import select

from models import Plan
from db import SessionDep

router = APIRouter()

@router.post("/plans", tags=["Plans"])
async def create_plan(plan_data: Plan , session: SessionDep):
    plan = Plan.model_validate(plan_data.model_dump())
    session.add(plan)
    session.commit()
    session.refresh(plan)
    return plan

@router.get("/plans", tags=["Plans"])
async def get_plans(session: SessionDep):
    statement = select(Plan)
    plans = session.exec(statement).all()
    
    if not plans:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No plans found")
    return plans