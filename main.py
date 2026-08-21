from fastapi import Depends, FastAPI
from sqlmodel import Session

from db import create_db, get_session
from models import Order, OrderItem, Product, User
from requests import (
    create_order,
    create_order_item,
    create_product,
    create_user,
    get_all_products,
    get_all_users,
    get_order_items_by_order_id,
    get_orders_by_user_id,
    get_product_by_id,
    get_user_by_id,
)

app = FastAPI(title="Deliversy API")

@app.on_event("startup")
def on_startup():
    create_db()

@app.post("/users", response_model=User)
def post_user(username:str, email:str, session: Session = Depends(get_session)):
    user = create_user(username, email, session)
    return user

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = get_user_by_id(user_id, session)
    return user

@app.get("/users", response_model=list[User])
def get_users(session: Session = Depends(get_session)):
    users = get_all_users(session)
    return users

@app.post("/products", response_model=Product)
def post_product(name: str, description: str, price: float, quantity: int, session: Session = Depends(get_session)):
    product = create_product(name, description, price, quantity, session)
    return product

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int, session: Session = Depends(get_session)):
    product = get_product_by_id(product_id, session)
    return product

@app.get("/products", response_model=list[Product])
def get_products(session: Session = Depends(get_session)):
    products = get_all_products(session)
    return products

@app.post("/orders", response_model=Order)
def post_order(user_id: int, session: Session = Depends(get_session)):
    order = create_order(user_id, session)
    return order

@app.get("/orders/{user_id}", response_model=list[Order])
def get_orders(user_id: int, session: Session = Depends(get_session)):
    order = get_orders_by_user_id(user_id, session)
    return order

@app.post("/order_items", response_model=OrderItem)
def post_order_item(order_id: int, product_id: int, quantity:int, session: Session = Depends(get_session)):
    order_item = create_order_item(order_id, product_id, quantity, session)
    return order_item

@app.get("/order_items/{order_id}", response_model=list[OrderItem])
def get_order_items(order_id: int, session: Session = Depends(get_session)):
    order_items = get_order_items_by_order_id(order_id, session)
    return order_items
