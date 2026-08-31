from sqlalchemy.orm import Session
from sqlmodel import select

from delivery.models import Courier, Delivery, DeliveryStatus


def create_delivery(order_id: int, courier_id: int, session: Session) -> Delivery:
    delivery = Delivery(order_id=order_id, courier_id=courier_id)
    session.add(delivery)
    session.commit()
    session.refresh(delivery)
    return delivery

def get_delivery_by_id(delivery_id: int, session: Session) -> Delivery:
    result = session.execute(
        select(Delivery).where(Delivery.id == delivery_id)
    )
    delivery = result.scalars().first()
    return delivery

def change_delivery_status(delivery_id: int, status: DeliveryStatus, session: Session) -> Delivery:
    delivery = get_delivery_by_id(delivery_id, session)
    delivery.sqlmodel_update({"status": status})

    session.add(delivery)
    session.commit()
    session.refresh(delivery)

    return delivery

def create_courier(name: str, session: Session) -> Courier:
    courier = Courier(name=name, session=session)
    session.add(courier)
    session.commit()
    session.refresh(courier)
    return courier

def get_courier_by_id(courier_id: int, session: Session) -> Courier:
    result = session.execute(
        select(Courier).where(Courier.id == courier_id)
    )
    courier = result.scalars().first()
    return courier

def get_all_couriers(session: Session) -> list[Courier]:
    result = session.execute(select(Courier).order_by(Courier.id))
    couriers = result.scalars().all()
    return couriers
