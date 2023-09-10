from pydantic import BaseModel, ConfigDict, EmailStr, Field, validator
from app.utils import validators as val


class UserBase(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
    )

    email: EmailStr


class Username(BaseModel):
    username: str = Field(min_length=4, max_length=20)

    @validator("username")
    def username_validate(cls, username: str) -> str:
        val.username_validate(username)
        return username


class Password(BaseModel):
    password: str = Field(min_length=8, max_length=90)

    @validator("password")
    def password_validate(cls, password: str) -> str:
        val.password_validate(password)
        return password
