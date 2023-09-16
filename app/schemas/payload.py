from app.schemas.base import PayloadBase
from app.settings.constance import USER_ROUTE_URI, PRODUCT_ROUTER_API


class Link(PayloadBase):
    detail: str
    href: str
    method: str = "GET"


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
            method="POST",
        ),
        Link(
            detail="delete you profile, you only delete self profile",
            href=USER_ROUTE_URI + "/<input username>/delete",
            method="DELETE",
        ),
        Link(
            detail="get all products specific user",
            href=USER_ROUTE_URI + "/<input username>/products",
        ),
    ]


class PayloadForProduct(PayloadBase):
    links: list[Link] = [
        Link(
            detail="get all products, you can add limit and offset params to url",
            href=PRODUCT_ROUTER_API + "?limit=10&offset=1",
        ),
        Link(
            detail="get product by ID", href=PRODUCT_ROUTER_API + "/<input product ID>"
        ),
        Link(detail="create your product", href=PRODUCT_ROUTER_API, method="POST"),
    ]
