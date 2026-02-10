from typing import Annotated
from contextlib import asynccontextmanager # Required for lifespan
from fastapi import FastAPI
from fastapi.params import Depends
from sqlmodel import Session, create_engine, SQLModel

from models import Customer, Transaction, Invoice

sqlite_name = "db.sqlite3"
sqlite_url = f"sqlite:///{sqlite_name}"

engine = create_engine(sqlite_url, echo=True)

# 2. Corrected Lifespan Function
@asynccontextmanager
async def create_all_tables(app: FastAPI):
    # This runs when the app starts
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    yield
    # This runs when the app shuts down
    print("Shutting down...")

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]