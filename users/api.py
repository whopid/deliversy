from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session

from users.db import create_users_db, get_users_session
from users.models import Address, User
from users.requests import (
    create_user,
    create_user_address,
    delete_address,
    get_addresses,
    get_all_users,
    get_user_by_id,
    verify_password,
)
from users.security import create_access_token


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_users_db()

    yield

app = FastAPI(title="Users API", lifespan=lifespan)

@app.post("/users", response_model=User)
async def post_user(username: str, email: str, password: str, session: Session = Depends(get_users_session)):
    user = create_user(username, email, password, session)
    return user

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int, session: Session = Depends(get_users_session)):
    if not (user := get_user_by_id(user_id, session)):
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users", response_model=list[User])
async def get_users(session: Session = Depends(get_users_session)):
    if not (users := get_all_users(session)):
        raise HTTPException(status_code=404, detail="Users not found")
    return users

@app.post("/users/{user_id}/addresses", response_model=Address)
async def post_user_address(address:str, user_id: int, session: Session = Depends(get_users_session)):
    address = create_user_address(address, user_id, session)
    return address

@app.get("/users/{user_id}/addresses", response_model=list[Address])
async def get_user_addresses(user_id: int, session: Session = Depends(get_users_session)):
    if not (address := get_addresses(user_id, session)):
        raise HTTPException(status_code=404, detail="Addresses not found")
    return address

@app.delete("/users/{user_id}/addresses/{address_id}", response_model=Address)
async def delete_user_address(user_id: int, address_id: int, session: Session = Depends(get_users_session)):
    address = delete_address(user_id, address_id, session)
    return address

@app.post("/auth/login", response_model=dict)
async def auth_user(email: str, password: str, session: Session = Depends(get_users_session)):
    if not verify_password(email, password, session):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    token = create_access_token(email)

    return {
        "access_token": token,
        "token_type": "bearer",
    }
