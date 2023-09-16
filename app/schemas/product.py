from typing import Optional
from datetime import datetime

from app.schemas.user import UserResponseInfo
from app.schemas.base import ProductBase
from app.schemas.payload import PayloadForProduct


class Product(ProductBase):
    id: int
    title: str
    description: str
    price: float
    created_on: datetime
    owner: UserResponseInfo
    payload: Optional[PayloadForProduct] = None


class ProductList(ProductBase):
    products: list[Product]
    payload: Optional[PayloadForProduct] = None


class ProductCreate(ProductBase):
    title: str
    description: str
    price: float

