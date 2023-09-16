from pydantic import BaseModel, ConfigDict, EmailStr, Field, validator
from app.utils import validators as val
from app.settings import constance as c


class UserBase(BaseModel):
    """
    Base scheme for work with users
    """

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
    )

    email: EmailStr


class PayloadBase(BaseModel):
    """
    Base scheme for work with payload which is added to responses
    """

    model_config = ConfigDict(from_attributes=True, extra="allow")


class ProductBase(BaseModel):
    """
    Base scheme for work with products
    """

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
    )


class Username(BaseModel):
    username: str = Field(
        min_length=c.MIN_USERNAME_LENGHT, max_length=c.MAX_USERNAME_LENGHT
    )

    @validator("username")
    def username_validate(cls, username: str) -> str:
        val.username_validate(username)
        return username


class Password(BaseModel):
    password: str = Field(
        min_length=c.MIN_PASSWORD_LENGHT, max_length=c.MAX_PASSWORD_LENGHT
    )

    @validator("password")
    def password_validate(cls, password: str) -> str:
        val.password_validate(password)
        return password
