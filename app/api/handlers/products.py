from fastapi import APIRouter, Depends, Query

from typing import Annotated

from app.settings.constance import PRODUCT_ROUTER_API
from app.auth.actions import get_current_user
from app.schemas.product import Product as ProductSchema, ProductList
from app.database.connect import get_session
from app.database.db import Database
from app.database.models.user import User
from app.database.models.product import Product
from app.schemas.user import UserResponseInfo


router = APIRouter(
    prefix=PRODUCT_ROUTER_API,
    tags=["products"],
    dependencies=[Depends(get_current_user)],
)


@router.get(
    "/",
    response_model=ProductList,
    status_code=200,
    response_description="Return all products",
)
async def get_all_products(
    limit: Annotated[
        int, Query(ge=1, le=100, description="number of results to be returned")
    ] = 10,
    offset: Annotated[
        int, Query(ge=1, le=100000, description="starting from number")
    ] = 1,
):
    async with get_session() as session:
        database = Database(session)
        products: list[Product] = await database.get_products(
            limit=limit, offset=offset - 1
        )
        response_list: list[ProductSchema] = []
        for product in products:
            # get the product owner
            owner: User = await database.get_user_by_id(product.user_id)
            # generate schema
            response_list.append(
                ProductSchema(
                    id=product.id,
                    title=product.title,
                    description=product.description,
                    price=product.price,
                    create_on=product.created_on,
                    owner=UserResponseInfo(
                        username=owner.username,
                        email=owner.email,
                        create_on=owner.created_on,
                    ),
                )
            )
    return ProductList(products=response_list)
