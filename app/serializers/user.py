from app.utils.helpers import hashed_password
from app.schemas.user import UserInfo
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
        self.data = data

    def to_save_in_db(self) -> Dict[str, str]:
        """
        serialize user data before save in DB
        """
        data_to_dict = dict(self.data)
        hash_password = hashed_password(data_to_dict.pop("password"))
        data_to_dict.update({"hash_password": hash_password})

        return data_to_dict

    def responce_user_info(self) -> UserInfo:
        """
        serialize database user model to schema UserInfo
        """
        user: User = self.data
        create_on = self.serialize_datatime_field(user.created_on)
        return UserInfo(
            email=user.email,
            username=user.username,
            create_on=create_on,
            payload=PayloadResponse(links=link_user_response()),
        )

    def response_user_info_list(self) -> list[UserInfo]:
        """
        serilize list with user models to list with UserInfo schemas
        and add payload to each object
        """
        users: list[User] = self.data
        serialize_users_list = [
            UserInfo(
                email=user.email,
                username=user.username,
                create_on=self.serialize_datatime_field(user.created_on),
                payload=PayloadResponse(links=link_user_response(user.username)),
            )
            for user in users
        ]
        return serialize_users_list

    def serialize_datatime_field(self, datetime_obj: datetime) -> str:
        """
        transform datetime to string
        """
        create_on = datetime_obj.strftime("%A, %B %d, %Y %I:%M:%S")
        return create_on
