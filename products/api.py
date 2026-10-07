from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session

from products.db import create_products_db, get_products_session
from products.models import Product
from products.requests import create_product, get_all_products, get_product_by_id, reserve_product

app = FastAPI(title="Products API")

@app.on_event("startup")
def on_startup():
    create_products_db()

@app.post("/products", response_model=Product)
async def post_product(name: str, description: str, price: float, quantity: int, session: Session = Depends(get_products_session)):
    product = create_product(name, description, price, quantity, session)
    return product

@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int, session: Session = Depends(get_products_session)):
    if not (product := get_product_by_id(product_id, session)):
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/products", response_model=list[Product])
async def get_products(session: Session = Depends(get_products_session)):
    if not (products := get_all_products(session)):
        raise HTTPException(status_code=404, detail="Products not found")
    return products

@app.post("/products/{product_id}/reserve", response_model=Product)
async def reserve(product_id: int, quantity: int, session: Session = Depends(get_products_session)):
    product = reserve_product(product_id, quantity, session)
    return product
