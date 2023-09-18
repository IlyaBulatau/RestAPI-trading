from pydantic import BaseModel, Field

from typing import Dict


class Desciption(BaseModel):
    """
    Schema for description exeptions
    """

    field: str | None
    text: str | None


class UserExeptionResponse(BaseModel):
    """
    response scheme when a user enters an existing email during registration
    """

    title: str = Field(alias="title", description="Title http exeption")
    status: int = Field(alias="status", description="Http response status")
    description: Dict = Field(
        alias="description", description="The field include data about invalid email"
    )
