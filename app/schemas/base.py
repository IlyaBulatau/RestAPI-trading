from pydantic import BaseModel, ConfigDict
from app.utils import validators as val


class UserBase(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
    )

    
