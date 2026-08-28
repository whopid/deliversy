from datetime import datetime

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    email: str
    password_hash: bytes
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Address(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int
    address: str
