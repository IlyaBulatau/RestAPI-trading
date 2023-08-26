from pydantic import BaseModel, EmailStr, Field, validator, UUID4

import re
import uuid


class UserBase(BaseModel):
    """
    Base user model
    """
    username: str = Field(alias="login", 
                          title="Username", 
                          description="Username for registration process",
                          min_length=4,
                          max_length=20)
    email: EmailStr
    
    @validator("username")
    def username_validate(cls, username: str) -> str:
        result = re.match(r"^[a-zA-Z0-9]+([_ -]?[a-zA-Z0-9])*$", username)
        if not result:
            raise ValueError("Username must be a word or set of words separated by 1 space or underscore")
        return username
    

class UserAuth(UserBase):
    """
    User schema for signup process
    """
    password: str = Field(alias="password", 
                          title="Password",
                          description="User password",
                          min_length=8,
                          max_length=90)
    
    
    @validator("password")
    def password_validate(cls, password: str) -> str:
        result = re.match(r'^.*(?=.{8,})(?=.*[a-zA-Z])(?=.*\d)(?=.*[!#$%&? "]).*$', password)
        if not result:
            raise ValueError("the Password must be more than 8 characters long and contain letters of the English alphabet numbers and special characters")
        return password


class UserResponce(UserBase):
    """
    User schema for answer after signup process
    """
    id: UUID4 = Field(default_factory=uuid.uuid4)

