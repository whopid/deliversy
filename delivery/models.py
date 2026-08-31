from datetime import datetime
from enum import Enum

from sqlmodel import Field, SQLModel


class CourierStatus(str, Enum):
    AVAILABLE = "available"
    BUSY = "busy"

class Courier(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    status: CourierStatus = Field(default=CourierStatus.AVAILABLE)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class DeliveryStatus(str, Enum):
    WAITING = "waiting"
    ASSIGNED = "assigned"
    PICKED_UP = "picked_up"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class Delivery(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    order_id: int
    courier_id: int
    status: DeliveryStatus = Field(default=DeliveryStatus.WAITING)
    created_at: datetime = Field(default_factory=datetime.utcnow)

