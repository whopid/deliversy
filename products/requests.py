from sqlmodel import Session, select

from products.models import Product


class ProductNotFound(Exception):
    pass

class NotEnoughProducts(Exception):
    pass

def get_all_products(session: Session) -> list[Product]:
    products = session.exec(select(Product)).all()
    return products

def get_product_by_id(product_id: int, session: Session) -> Product:
    product = session.exec(select(Product).where(Product.id == product_id)).first()
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

def reserve_product(
        product_id: int,
        quantity: int,
        session: Session
) -> Product:
    product = session.exec(
        select(Product)
        .where(Product.id == product_id)
        .with_for_update()
    ).one_or_none()

    if product is None:
        raise ProductNotFound()

    if product.quantity < quantity:
        raise NotEnoughProducts()

    product.quantity -= quantity

    session.commit()
    session.refresh(product)

    return product
