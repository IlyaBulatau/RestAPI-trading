from app.schemas.base import PayloadBase

from pydantic import Field


class Link(PayloadBase):
    detail: str
    href: str


class Payload(PayloadBase):
    links: list[Link]
