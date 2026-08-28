from sqlalchemy.orm import Session
from sqlmodel import select

from products.models import Product


def get_all_products(session: Session) -> list[Product]:
    result = session.execute(
        select(Product)
    )
    result = result.scalars().all()
    return result

def get_product_by_id(product_id: int, session: Session) -> Product:
    result = session.execute(
        select(Product).where(Product.id == product_id)
    )
    product = result.scalars().first()
    return product

def create_product(
        name: str,
        description: str,
        price: float,
        quantity: int,
        session: Session
) -> Product:
    product = Product(name=name, description=description, price=price, quantity=quantity)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product
