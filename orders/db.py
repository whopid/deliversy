from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel

from env import ORDERS_DATABASE_URL
from orders.models import Order, OrderItem

orders_engine = create_engine(ORDERS_DATABASE_URL, echo=True)

orders_session_maker = sessionmaker(
    bind=orders_engine,
    class_=Session,
    autocommit=False,
    autoflush=False,
)

def create_orders_db():
    SQLModel.metadata.create_all(
        orders_engine,
        tables=[Order.__table__, OrderItem.__table__],
    )

def get_orders_session():
    with orders_session_maker() as session:
        yield session
