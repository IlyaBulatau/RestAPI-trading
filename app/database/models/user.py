import sqlalchemy as db
from sqlalchemy.sql.functions import func
from sqlalchemy import orm

from uuid import uuid4

from app.database.models.product import Product
from app.database.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: orm.Mapped[db.UUID] = orm.mapped_column(
        db.UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    username: orm.Mapped[str] = orm.mapped_column(
        db.String(length=30), nullable=False, unique=True
    )
    email: orm.Mapped[str] = orm.mapped_column(
        db.String(length=90), unique=True, nullable=False
    )
    hash_password: orm.Mapped[str] = orm.mapped_column(
        db.String(length=90), nullable=False
    )
    products = orm.relationship("Product", back_populates="user")
