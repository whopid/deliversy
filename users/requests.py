import bcrypt
from sqlmodel import Session, select

from users.models import Address, User


def create_user(username: str, email: str, password: str, session: Session) -> User:
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    user = User(username=username, email=email, password_hash=password_hash)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_user_by_id(user_id: int, session: Session) -> User:
    user = session.exec(select(User).where(User.id == user_id)).first()
    return user

def get_all_users(session: Session) -> list[User]:
    users = session.exec(select(User)).all()
    return users

def create_user_address(address: str, user_id: int, session: Session) -> Address:
    address = Address(user_id=user_id, address=address)
    session.add(address)
    session.commit()
    session.refresh(address)
    return address

def get_addresses(user_id: int, session: Session) -> list[Address]:
    addresses = session.exec(select(Address).where(Address.user_id == user_id)).all()
    return addresses

def delete_address(user_id: int, address_id: int, session: Session) -> Address:
    address = session.exec(select(Address).where(Address.id == address_id)).first()
    session.delete(address)
    session.commit()
    session.refresh(address)
    return address

def verify_password(email: str, password: str, session: Session) -> bool:
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        return False
    return bcrypt.checkpw(password.encode("utf-8"), user.password_hash)
