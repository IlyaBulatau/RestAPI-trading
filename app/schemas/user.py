from pydantic import BaseModel, EmailStr, Field, validator, UUID4
from app.utils import validators as val

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
    password: str = Field(alias="password", 
                          title="Password",
                          description="User password",
                          min_length=8,
                          max_length=90)
    
    @validator("password")
    def password_validate(cls, password: str) -> str:
        val.password_validate(password)
        return password


class UserResponceBase(UserBase):
    """
    Base model for responce process user
    :email
    :id
    :username
    """
    id: UUID4 = Field(default_factory=uuid.uuid4)
    username: str = Field(alias="login", 
                          title="Username", 
                          description="Username for responce")
    

class UserAuth(UserAuthBase):
    """
    User schema for signup process
    :email
    :password
    :username
    """
    username: str = Field(alias="login", 
                          title="Username", 
                          description="Username for registration process",
                          min_length=4,
                          max_length=20)
    
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
        super().password_validate(UserLogin, password)


class UserResponce(UserResponceBase):
    """
    User schema for answer after signup process
    :email
    :username
    :id
    """
    pass


