from pydantic import BaseModel, Field

from datetime import datetime


class LinkDetailResponse(BaseModel):
    """
    information about URIs
    """

    route: str = Field(description="Path to endpoint")
    description: str = Field(description="message about the endpoint")


class LinkResponse(BaseModel):
    """
    Add hipermedia links for responses
    """

    title: str = Field(description="Endpoint Title")
    detail: LinkDetailResponse = Field(description="Info about the URI")


class PayloadResponse(BaseModel):
    """
    Payload model for responses
    """

    time_now: datetime = Field(default=datetime.now(), description="datetime Field")
    links: list[LinkResponse] | list = Field(default=[], description="useful links")
