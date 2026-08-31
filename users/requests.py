import bcrypt
from sqlalchemy.orm import Session
from sqlmodel import select

from users.models import Address, User


def create_user(username: str, email: str, password: str, session: Session) -> User:
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    user = User(username=username, email=email, password_hash=password_hash)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_user_by_id(user_id: int, session: Session) -> User:
    result = session.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalars().first()
    return user

def get_all_users(session: Session) -> list[User]:
    result = session.execute(select(User))
    result = result.scalars().all()
    return result

def create_user_address(address: str, user_id: int, session: Session) -> Address:
    address = Address(user_id=user_id, address=address)
    session.add(address)
    session.commit()
    session.refresh(address)
    return address

def get_addresses(user_id: int, session: Session) -> list[Address]:
    result = session.execute(
        select(Address).where(Address.user_id == user_id)
    )
    result = result.scalars().all()
    return result

def delete_address(user_id: int, address_id: int, session: Session) -> Address:
    address = session.execute(
        select(Address).where(Address.id == address_id)
    )
    address = address.scalars().first()
    session.delete(address)
    session.commit()
    session.refresh(address)
    return address

def verify_password(email: str, password: str, session: Session) -> bool:
    user = session.execute(
        select(User).where(User.email == email)
    ).scalars().first()
    if not user:
        return False
    return bcrypt.checkpw(password.encode("utf-8"), user.password_hash)
