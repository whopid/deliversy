from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session

from delivery.db import create_delivery_db, get_delivery_session
from delivery.models import Courier, Delivery, DeliveryStatus
from delivery.requests import (
    change_delivery_status,
    create_courier,
    create_delivery,
    get_all_couriers,
    get_courier_by_id,
    get_delivery_by_id,
)

app = FastAPI(title="Delivery API")

@app.on_event("startup")
def on_startup():
    create_delivery_db()

@app.post("/deliveries", response_model=Delivery)
def post_delivery(order_id: int, courier_id: int,  session: Session = Depends(get_delivery_session)):
    delivery = create_delivery(order_id, courier_id, session)
    return delivery

@app.get("/deliveries/{delivery_id}", response_model=Delivery)
def get_delivery(delivery_id: int, session: Session = Depends(get_delivery_session)):
    if not (delivery := get_delivery_by_id(delivery_id, session)):
        raise HTTPException(status_code=404, detail="Delivery not found")
    return delivery

@app.patch("/deliveries/{delivery_id}/status", response_model=Delivery)
def patch_delivery_status(delivery_id: int, status: DeliveryStatus, session: Session = Depends(get_delivery_session)):
    delivery = change_delivery_status(delivery_id, status, session)
    return delivery

@app.post("/couriers", response_model=Courier)
def post_courier(name: str, session: Session = Depends(get_delivery_session)):
    courier = create_courier(name, session)
    return courier

@app.get("/couriers/{courier_id}", response_model=Courier)
def get_courier(courier_id: int, session: Session = Depends(get_delivery_session)):
    if not (courier := get_courier_by_id(courier_id, session)):
        raise HTTPException(status_code=404, detail="Courier not found")
    return courier

@app.get("/couriers", response_model=list[Courier])
def get_couriers(session: Session = Depends(get_delivery_session)):
    if not (couriers := get_all_couriers(session)):
        raise HTTPException(status_code=404, detail="Couriers not found")
    return couriers
