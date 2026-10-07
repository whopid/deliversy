from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel

from delivery.models import Courier, Delivery
from env import DELIVERY_DATABASE_URL

delivery_engine = create_engine(DELIVERY_DATABASE_URL, echo=True)

delivery_session_maker = sessionmaker(
    bind=delivery_engine,
    class_=Session,
    autocommit=False,
    autoflush=False,
)

def create_delivery_db():
    SQLModel.metadata.create_all(
        delivery_engine,
        tables=[Courier.__table__, Delivery.__table__],
    )

def get_delivery_session():
    with delivery_session_maker() as session:
        yield session
