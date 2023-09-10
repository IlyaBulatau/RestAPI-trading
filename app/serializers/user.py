from app.utils.helpers import hashed_password
from app.schemas.responses import PayloadResponse
from app.database.models.user import User
from app.servise.payload_links import link_user_response

from typing import Dict, Any

from datetime import datetime


class UserSerializer:
    """
    serialize data for work with user
    """

    def __init__(self, data: Any):
        self.data: dict = data

    def to_save_in_db(self) -> Dict[str, str]:
        """
        serialize user data before save in DB
        """
        data = self.data
        hash_password = hashed_password(data.pop("password"))
        data.update({"hash_password": hash_password})

        return data


    def serialize_datatime_field(self, datetime_obj: datetime) -> str:
        """
        transform datetime to string
        """
        create_on = datetime_obj.strftime("%A, %B %d, %Y %I:%M:%S")
        return create_on
