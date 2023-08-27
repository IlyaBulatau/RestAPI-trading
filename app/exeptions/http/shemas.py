from pydantic import BaseModel, Field

from typing import Dict, Any

class Desciption(BaseModel):
    """
    Schema for description exeptions
    """
    field: str | None
    text: str | None


class UserEmailNotFoundResponse(BaseModel):
    """
    response scheme when a user enters an existing email during registration
    """
    title: str = Field(alias="title",
                       description="Title http exeption")
    status: int = Field(alias="status",
                        description="Http response status")
    description: Dict = Field(alias="detail",
                              description="The field include data about invalid email")
    