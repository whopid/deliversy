from sqlalchemy.orm import Session
from sqlmodel import select

from models import Order, OrderItem, Product, User


def get_user_by_id(user_id: int, session: Session) -> User:
    result = session.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalars().first()
    return user

def get_all_users(session: Session) -> list[User]:
    result = session.execute(
        select(User)
    )
    result = result.scalars().all()
    return result

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

def get_orders_by_user_id(user_id: int, session: Session) -> list[Order]:
    result = session.execute(
        select(Order).where(Order.user_id == user_id)
    )
    product = result.scalars().all()
    return product

def get_order_items_by_order_id(order_id: int, session: Session) -> list[OrderItem]:
    result = session.execute(
        select(OrderItem).where(OrderItem.order_id == order_id)
    )
    product = result.scalars().all()
    return product

def create_user(username:str, email:str, session: Session) -> User:
    user = User(username=username, email=email)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

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

def create_order(user_id: int, session: Session) -> Order:
    order = Order(user_id=user_id)
    session.add(order)
    session.commit()
    session.refresh(order)
    return order

def create_order_item(
        order_id: int,
        product_id: int,
        quantity: int,
        session: Session
) -> OrderItem:
    order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=quantity)
    session.add(order_item)
    session.commit()
    session.refresh(order_item)
    return order_item
