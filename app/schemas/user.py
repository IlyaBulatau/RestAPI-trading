from pydantic import BaseModel, UUID4, Field, EmailStr

from app.schemas.base import UserBase, Username, Password
from app.schemas.payload import PayloadForUser

from datetime import datetime
from typing import Optional


class UserAuth(UserBase, Username, Password):
    """
    Schema for auth processe
    Field:
    - email
    - username
    - password
    """

    pass


class UserLogin(UserBase, Password):
    """
    Schema for login pocesse
    Field:
    - email
    - password
    """

    pass


class UserAuthResponse(UserBase, Username):
    """
    Schema for responses after auth process
    Field:
    - id
    - email
    - username
    - payload[opt]
    """

    id: UUID4
    payload: Optional[PayloadForUser] = []


class UserResponseInfo(UserBase, Username):
    """
    Schema for response user info
    Field:
    - email
    - username
    - create_on
    - payload[opt]
    """

    create_on: datetime
    payload: Optional[PayloadForUser] = []


class UserUpdate(UserBase, Username):
    """
    Schema for update user endpoint
    Field:
    - email[opt]
    - username[opt]
    """

    email: EmailStr | None = Field(default=None)
    username: str | None = Field(default=None)


class UserList(BaseModel):
    """
    Schema for response list users
    Field:
    - users
    """

    users: list[UserResponseInfo]
    payload: Optional[PayloadForUser] = []
