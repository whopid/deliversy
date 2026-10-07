from contextlib import asynccontextmanager

import httpx
from fastapi import Depends, FastAPI, HTTPException, Request
from sqlmodel import Session

from orders.db import create_orders_db, get_orders_session
from orders.models import Order, OrderItem, ProductResponse
from orders.requests import (
    create_order,
    create_order_item,
    get_order_items_by_order_id,
    get_orders_by_user_id,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_orders_db()

    app.state.user_client = httpx.AsyncClient(
        base_url="http://localhost:8001"
    )
    app.state.product_client = httpx.AsyncClient(
        base_url="http://localhost:8002"
    )

    yield

    await app.state.user_client.aclose()
    await app.state.product_client.aclose()

app = FastAPI(title="Orders API", lifespan=lifespan)

@app.post("/orders", response_model=Order)
async def post_order(
        user_id: int,
        total_price: float,
        delivery_address: str,
        request: Request,
        session: Session = Depends(get_orders_session)
):
    user_client: httpx.AsyncClient = request.app.state.user_client

    response = await user_client.get(f"/users/{user_id}")

    if response.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    response.raise_for_status()

    order = create_order(
        user_id,
        total_price,
        delivery_address,
        session,
    )

    return order

@app.get("/orders/{user_id}", response_model=list[Order])
async def get_orders(user_id: int, session: Session = Depends(get_orders_session)):
    if not (order := get_orders_by_user_id(user_id, session)):
        raise HTTPException(status_code=404, detail="Orders not found")
    return order

@app.post("/order_items", response_model=OrderItem)
async def post_order_item(
        order_id: int,
        product_id: int,
        quantity: int,
        request: Request,
        session: Session = Depends(get_orders_session)
):
    client: httpx.AsyncClient = request.app.state.product_client

    reserve_response = await client.post(
        f"/products/{product_id}/reserve",
        params={"quantity": quantity},
    )

    if reserve_response.status_code == 409:
        raise HTTPException(
            status_code=409,
            detail="Not enough items for this product",
        )

    reserve_response.raise_for_status()
    product = ProductResponse.model_validate(
        reserve_response.json()
    )

    order_item = create_order_item(order_id, product_id, product.name, product.price, quantity, session)
    return order_item

@app.get("/order_items/{order_id}", response_model=list[OrderItem])
async def get_order_items(order_id: int, session: Session = Depends(get_orders_session)):
    if not (order_items := get_order_items_by_order_id(order_id, session)):
        raise HTTPException(status_code=404, detail="Order items not found")
    return order_items
