from fastapi import APIRouter, Depends, Query, Path, HTTPException, status

from typing import Annotated

from app.settings.constance import PRODUCT_ROUTER_API
from app.auth.actions import get_current_user
from app.schemas.product import Product as ProductSchema, ProductList
from app.database.connect import get_session
from app.database.managers import ProductManager
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
        database = ProductManager(session)
        products: list[Product] = await database.get_products(
            limit=limit, offset=offset - 1
        )
    return ProductList(
        products=[
            ProductSchema(
                id=product.id,
                title=product.title,
                description=product.description,
                price=product.price,
                create_on=product.created_on,
                owner=UserResponseInfo(
                    username=product.owner.username,
                    email=product.owner.email,
                    create_on=product.owner.created_on,
                ),
            )
            for product in products
        ]
    )


@router.get(
    "/{product_id}",
    response_model=ProductSchema,
    status_code=200,
    response_description="Return the product by id",
)
async def get_product_by_id(
    product_id: Annotated[int, Path(ge=0, description="ID the product")]
):
    async with get_session() as session:
        database = ProductManager(session)
        product: Product = await database.get_product_by_id(product_id=product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Product Not Found"
        )

    return ProductSchema(
        id=product_id,
        title=product.title,
        description=product.description,
        price=product.price,
        create_on=product.created_on,
        owner=UserResponseInfo(
            username=product.owner.username,
            email=product.owner.email,
            create_on=product.owner.created_on,
        ),
    )
