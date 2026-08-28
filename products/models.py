from datetime import datetime

from sqlmodel import Field, SQLModel


class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    price: float
    quantity: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
