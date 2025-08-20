from sqlmodel import SQLModel, Field, create_engine, Session
import os

DB_PATH = os.environ.get("LL_DB_PATH", "ledgerlens.db")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)
