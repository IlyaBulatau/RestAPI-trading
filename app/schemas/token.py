from pydantic import BaseModel, EmailStr, Field

from app.schemas.responses import PayloadResponse

from datetime import datetime


class Token(BaseModel):
    token: str
    type: str = "Bearer"
    payload: PayloadResponse = Field(default_factory=PayloadResponse)


class Payload(BaseModel):
    user_id: str
    email: EmailStr
    exp: datetime | None = None
