import sqlalchemy as db
from sqlalchemy.sql.functions import func

from uuid import uuid4

from app.database.models.base import Base

class User(Base):
    __tablename__ = "users"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = db.Column(db.String(), nullable=False, unique=True)
    hash_password = db.Column(db.String(), nullable=False, unique=True)
    created_on = db.Column(db.DateTime(), default=func.now())
    update__on = db.Column(db.DateTime(), default=func.now(), onupdate=func.now())