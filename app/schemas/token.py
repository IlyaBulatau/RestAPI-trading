from pydantic import BaseModel, EmailStr, Field


from datetime import datetime


class Token(BaseModel):
    token: str
    type: str = "Bearer"


class Payload(BaseModel):
    user_id: str
    email: EmailStr
    exp: datetime | None = None
