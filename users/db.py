from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlmodel import SQLModel

from env import USERS_DATABASE_URL
from users.models import User

users_engine = create_engine(USERS_DATABASE_URL, echo=True)

users_session_maker = sessionmaker(
    bind=users_engine,
    class_=Session,
    autocommit=False,
    autoflush=False,
)

def create_users_db():
    SQLModel.metadata.create_all(
        users_engine,
        tables=[User.__table__],
    )

def get_users_session():
    with users_session_maker() as session:
        yield session
