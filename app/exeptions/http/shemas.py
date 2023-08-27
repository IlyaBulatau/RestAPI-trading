from pydantic import BaseModel, Field


class UserExist(BaseModel):
    title: str = Field(alias="title",
                       description="Title http exeption")
    status: int = Field(alias="status",
                        description="Http response status")