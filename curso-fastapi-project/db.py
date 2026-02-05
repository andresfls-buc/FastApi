from typing import Annotated

from fastapi.params import Depends
from sqlmodel import create_engine
# we must import Session from sqlmodel, so pylance recognizes it correctly
from sqlmodel import Session, create_engine , SQLModel

sqlite_name = "db.sqlite3"
sqlite_url= f"sqlite:///{sqlite_name}"

#echo=True to see the SQL commands in the console
engine = create_engine(sqlite_url , echo=True)

def create_all_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]