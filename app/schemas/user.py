from pydantic import BaseModel, UUID4, Field, validator, EmailStr

from app.utils import validators as val
from app.schemas.responses import PayloadResponse
from app.schemas.base import UserBase, Username, Password

from datetime import datetime


class UserAuth(UserBase, Username, Password):
    pass


class UserLogin(UserBase, Password):
    pass


class UserAuthResponse(UserBase, Username):
    id: UUID4


class UserResponseInfo(UserBase, Username):
    create_on: datetime


class UserUpdate(UserBase, Username):
    email: EmailStr | None = Field(default=None)
    username: str | None = Field(default=None)


class UserList(BaseModel):
    users: list[UserResponseInfo]
