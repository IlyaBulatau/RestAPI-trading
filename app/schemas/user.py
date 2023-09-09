from pydantic import BaseModel, EmailStr, Field, validator, UUID4, ConfigDict

from app.utils import validators as val
from app.schemas.responses import PayloadResponse

from datetime import datetime
import uuid


class UserBase(BaseModel):
    """
    User base model
    :email
    """

    email: EmailStr


class UserAuthBase(UserBase):
    """
    Base models for auth processes user
    :email
    :password
    """

    password: str = Field(
        alias="password",
        title="Password",
        description="User password",
        min_length=8,
        max_length=90,
    )

    @validator("password")
    def password_validate(cls, password: str) -> str:
        val.password_validate(password)
        return password


class UserResponceBase(UserBase):
    """
    Base model for responce process user
    :email
    :username
    """

    username: str = Field(
        alias="username", 
        title="Username", 
        description="Username for responce",
        min_length=4,
        max_length=20,
    )


class UserAuth(UserAuthBase):
    """
    User schema for signup process
    :email
    :password
    :username
    """

    username: str = Field(
        alias="username",
        title="Username",
        description="Username for registration process",
        min_length=4,
        max_length=20,
    )

    @validator("username")
    def username_validate(cls, username: str) -> str:
        val.username_validate(username)
        return username


class UserLogin(UserAuthBase):
    """
    User schema for signin process
    :email
    :password
    """

    @validator("password")
    def password_validate(cls, password):
        super().password_validate(password)
        return password


class UserResponce(UserResponceBase):
    """
    User schema for answer after signup process
    :email
    :username
    :id
    """

    id: UUID4 = Field(default_factory=uuid.uuid4)
    payload: PayloadResponse = Field(default_factory=PayloadResponse)


class UserInfo(UserResponceBase):
    """
    User schema for response in gateway /api/me
    :email
    :username
    :create_on
    """

    create_on: datetime | str = Field(
        alias="create_on",
        title="create time",
        description="Create time user registration",
    )
    payload: PayloadResponse = Field(default_factory=PayloadResponse)


class UserList(BaseModel):
    users: list[UserInfo]
    payload: PayloadResponse = Field(default_factory=PayloadResponse)


class UserUpdate(UserResponceBase):
    model_config = ConfigDict(extra="forbid")

    username: str | None = Field(
            default=None,
            min_length=4,
            max_length=20
    )
    email: EmailStr | None = Field(
        default=None
    )

    @validator("username")
    def username_validate(cls, username: str) -> str:
        val.username_validate(username)
        return username


