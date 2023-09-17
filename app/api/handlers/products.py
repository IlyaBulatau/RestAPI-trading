from fastapi import APIRouter, Depends, Query, Path, HTTPException, status

from typing import Annotated

from app.servise.dependens import GET_CURRENT_USER
from app.settings.constance import PRODUCT_ROUTER_API, USER_ROUTE_URI
from app.auth.actions import get_current_user
from app.schemas.product import Product as ProductSchema, ProductList, ProductCreate
from app.schemas.payload import PayloadForUser, Link, PayloadForProduct
from app.database.connect import get_session
from app.database.managers import ProductManager
from app.database.models.product import Product
from app.schemas.user import UserResponseInfo
from app.servise.cache import cache, cache_reset


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
@cache()
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
                **database.model_dump(product),
                owner=UserResponseInfo(
                    username=product.owner.username,
                    email=product.owner.email,
                    create_on=product.owner.created_on,
                    payload=PayloadForUser(
                        links=[
                            Link(
                                detail="path to profile the user",
                                href=USER_ROUTE_URI + f"/{product.owner.username}",
                            )
                        ]
                    ),
                ),
            )
            for product in products
        ],
        payload=PayloadForProduct(),
    )


@router.get(
    "/{product_id}",
    response_model=ProductSchema,
    status_code=200,
    response_description="Return the product by id",
)
@cache()
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

    model_dump = database.model_dump(product)
    return ProductSchema(
        **model_dump,
        owner=UserResponseInfo(
            username=product.owner.username,
            email=product.owner.email,
            create_on=product.owner.created_on,
            payload=PayloadForUser(
                links=[
                    Link(
                        detail="path to profile the user",
                        href=USER_ROUTE_URI + f"/{product.owner.username}",
                    )
                ]
            ),
        ),
        payload=PayloadForProduct(),
    )


@router.post(
    "/",
    response_model=ProductSchema,
    status_code=201,
    response_description="Return the product after if has been created",
)
@cache_reset("get_all_products")
async def create_product(current_user: GET_CURRENT_USER, product: ProductCreate):
    async with get_session() as session:
        database = ProductManager(session)

        new_product: Product = await database.create_product(
            product.model_dump(), owner=current_user
        )

    model_dump = database.model_dump(new_product)
    return ProductSchema(
        **model_dump,
        owner=UserResponseInfo(
            username=current_user.username,
            email=current_user.email,
            create_on=current_user.created_on,
        ),
        payload=PayloadForProduct(),
    )
