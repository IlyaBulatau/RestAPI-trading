from app.schemas.base import PayloadBase
from app.settings.constance import USER_ROUTE_URI


class Link(PayloadBase):
    detail: str
    href: str


class PayloadForUser(PayloadBase):
    links: list[Link] = [
        Link(detail="get specific user", href=USER_ROUTE_URI + "/<input username>"),
        Link(detail="get you accaunt", href=USER_ROUTE_URI + "/me"),
        Link(
            detail="get all users, you can add limit and offset params to url",
            href=USER_ROUTE_URI + "?limit=10&offset=1",
        ),
        Link(
            detail="update data in you profile, you only update self profile",
            href=USER_ROUTE_URI + "/<input username>/update",
        ),
        Link(
            detail="delete you profile, you only delete self profile",
            href=USER_ROUTE_URI + "/<input username>/delete",
        ),
    ]
