from pydantic import BaseModel, UUID4, Field, validator, EmailStr

from app.utils import validators as val
from app.schemas.base import UserBase, Username, Password

from datetime import datetime


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
    """

    id: UUID4


class UserResponseInfo(UserBase, Username):
    """
    Schema for response user info
    Field:
    - email
    - username
    - create_on
    """

    create_on: datetime


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
