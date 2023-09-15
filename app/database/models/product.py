from sqlalchemy import orm
from sqlalchemy.sql.functions import func
import sqlalchemy as db

from app.database.models.base import Base


class Product(Base):
    __tablename__ = "products"

    id: orm.Mapped[db.Integer] = orm.mapped_column(db.Integer(), primary_key=True)
    title: orm.Mapped[db.String] = orm.mapped_column(db.String(), nullable=False)
    description: orm.Mapped[db.String] = orm.mapped_column(db.Text(), nullable=False)
    price: orm.Mapped[db.Float] = orm.mapped_column(
        db.Float(precision=2), nullable=False
    )
    user_id: orm.Mapped[db.UUID] = orm.mapped_column(
        db.UUID(as_uuid=True), db.ForeignKey("users.id")
    )
