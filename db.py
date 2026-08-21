from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlmodel import SQLModel

from env import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)

session_maker = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session
)

def create_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with session_maker() as session:
        yield session
