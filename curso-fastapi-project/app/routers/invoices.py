from models import Invoice
from fastapi import APIRouter , status
from db import SessionDep


router = APIRouter()

@router.post("/invoices" , status_code= status.HTTP_201_CREATED , tags=["Invoices"])
async def create_invoice(invoice_data: Invoice, session: SessionDep):
    invoice = Invoice.model_validate(invoice_data.model_dump())
    session.add(invoice)
    session.commit()
    session.refresh(invoice)
    return invoice
