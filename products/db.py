from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlmodel import SQLModel

from env import PRODUCTS_DATABASE_URL
from products.models import Product

products_engine = create_engine(PRODUCTS_DATABASE_URL, echo=True)

products_session_maker = sessionmaker(
    bind=products_engine,
    class_=Session,
    autocommit=False,
    autoflush=False,
)

def create_products_db():
    SQLModel.metadata.create_all(
        products_engine,
        tables=[Product.__table__],
    )

def get_products_session():
    with products_session_maker() as session:
        yield session
