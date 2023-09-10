from pydantic import BaseModel, EmailStr, UUID4, Field, validator

from app.utils import validators as val
from app.schemas.responses import PayloadResponse
from app.schemas.base import UserBase

from datetime import datetime



class UserAuth(UserBase):
    email: EmailStr
    username: str = Field(
        min_length=4,
        max_length=20
        )
    password: str = Field(
        min_length=8,
        max_length=90
    )

    @validator("username")
    def username_validate(cls, username: str) -> str:
        val.username_validate(username)
        return username

    @validator("password")
    def password_validate(cls, password: str) -> str:
        val.password_validate(password)
        return password



class UserLogin(UserBase):
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=90
    )

    @validator("password")
    def password_validate(cls, password: str) -> str:
        val.password_validate(password)
        return password



class UserAuthResponse(UserBase):
    id: UUID4
    email: EmailStr
    username: str = Field(
        min_length=4,
        max_length=20
        )

    @validator("username")
    def username_validate(cls, username: str) -> str:
        val.username_validate(username)
        return username


class UserResponseInfo(UserBase):
    email: EmailStr
    username: str = Field(
        min_length=4,
        max_length=20
        )
    create_on: datetime


    @validator("username")
    def username_validate(cls, username: str) -> str:
        val.username_validate(username)
        return username


class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None)
    username: str | None = Field(default=None)

    @validator("username")
    def username_validate(cls, username: str) -> str:
        val.username_validate(username)
        return username


class UserList(UserBase):
    users: list[UserResponseInfo]

