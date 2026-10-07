from datetime import datetime
from enum import Enum

from sqlmodel import Field, SQLModel


class OrderStatus(str, Enum):
    CREATED = "created"
    ASSIGNED = "assigned"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class Order(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int
    status: OrderStatus = Field(default=OrderStatus.CREATED)
    total_price: float
    delivery_address: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class OrderItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    order_id: int
    product_id: int
    product_name: str
    price: float
    quantity: int

class ProductResponse(SQLModel, table=False):
    id: int
    name: str
    description: str
    price: float
    quantity: int
    created_at: datetime

class OrderItemCreate(SQLModel, table=False):
    product_id: int
    quantity: int

class OrderCreate(SQLModel, table=False):
    user_id: int
    delivery_address: str
    items: list[OrderItemCreate]
