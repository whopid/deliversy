from sqlalchemy.orm import Session
from sqlmodel import select

from orders.models import Order, OrderItem


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
