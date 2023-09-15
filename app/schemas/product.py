from datetime import datetime

from app.schemas.user import UserResponseInfo
from app.schemas.base import ProductBase


class Product(ProductBase):
    id: int
    title: str
    description: str
    price: float
    create_on: datetime
    owner: UserResponseInfo


class ProductList(ProductBase):
    products: list[Product]
