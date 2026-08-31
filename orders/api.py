from fastapi import Depends, FastAPI
from sqlmodel import Session

from orders.db import create_orders_db, get_orders_session
from orders.models import Order, OrderItem
from orders.requests import (
    create_order,
    create_order_item,
    get_order_items_by_order_id,
    get_orders_by_user_id,
)

app = FastAPI(title="Orders API")

@app.on_event("startup")
def on_startup():
    create_orders_db()

@app.post("/orders", response_model=Order)
def post_order(user_id: int, total_price: float, delivery_address: str, session: Session = Depends(get_orders_session)):
    order = create_order(user_id, total_price, delivery_address, session)
    return order

@app.get("/orders/{user_id}", response_model=list[Order])
def get_orders(user_id: int, session: Session = Depends(get_orders_session)):
    order = get_orders_by_user_id(user_id, session)
    return order

@app.post("/order_items", response_model=OrderItem)
def post_order_item(order_id: int, product_id: int, product_name: str, price: float, quantity:int, session: Session = Depends(get_orders_session)):
    order_item = create_order_item(order_id, product_id, product_name, price, quantity, session)
    return order_item

@app.get("/order_items/{order_id}", response_model=list[OrderItem])
def get_order_items(order_id: int, session: Session = Depends(get_orders_session)):
    order_items = get_order_items_by_order_id(order_id, session)
    return order_items
