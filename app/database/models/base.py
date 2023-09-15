from sqlalchemy import orm
import sqlalchemy as db
from sqlalchemy.sql.functions import func

from datetime import datetime


class Base(orm.DeclarativeBase):
    __abstract__ = True

    created_on: orm.Mapped[datetime] = orm.mapped_column(
        db.DateTime(), server_default=func.now()
    )
    update_on: orm.Mapped[datetime] = orm.mapped_column(
        db.DateTime(), server_default=func.now(), onupdate=func.now()
    )
