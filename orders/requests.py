from sqlmodel import Session, select

from orders.models import Order, OrderItem


def get_orders_by_user_id(user_id: int, session: Session) -> list[Order]:
    orders = session.exec(select(Order).where(Order.user_id == user_id)).all()
    return orders

def get_order_items_by_order_id(order_id: int, session: Session) -> list[OrderItem]:
    order_items = session.exec(select(OrderItem).where(OrderItem.order_id == order_id)).all()
    return order_items

def create_order(user_id: int, total_price: float, delivery_address: str, session: Session) -> Order:
    order = Order(user_id=user_id, total_price=total_price, delivery_address=delivery_address)
    session.add(order)
    session.commit()
    session.refresh(order)
    return order

def create_order_item(
        order_id: int,
        product_id: int,
        product_name: str,
        price: float,
        quantity: int,
        session: Session
) -> OrderItem:
    order_item = OrderItem(order_id=order_id, product_id=product_id, product_name=product_name, price=price, quantity=quantity)
    session.add(order_item)
    session.commit()
    session.refresh(order_item)
    return order_item
