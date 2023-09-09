from fastapi import APIRouter, Depends

from typing import Annotated

from app.schemas.user import UserAuth, UserResponce
from app.schemas.responses import PayloadResponse, LinkResponse
from app.schemas.token import Token, Payload
from app.database import db
from app.database.models.user import User
from app.auth.actions import authenticate_user, is_exists_user
from app.utils.helpers import generate_token
from app.servise.payload_links import links_to_auth_process
from app.settings.constance import AUTH_ROUTE_URI


router = APIRouter(prefix=AUTH_ROUTE_URI, tags=["auth"])


@router.post(
    path="/signup",
    response_model=UserResponce,
    status_code=201,
    response_description="Responce userID, username and email",
)
async def signup_process(
    user: Annotated[UserAuth, Depends(is_exists_user)],
    links: Annotated[list[LinkResponse], Depends(links_to_auth_process)],
):
    """
    Handles registration process
    :user - user model form Database
    :links - list links(LinkResponse objects) for payload generated
    """
    user_id = await db.Database().create_user_in_db(user)
    return UserResponce(
        username=user.username,
        email=user.email,
        id=user_id,
        payload=PayloadResponse(links=links),
    )


@router.post(
    path="/signin",
    status_code=200,
    response_model=Token,
    response_description="Responce token",
)
async def signin_process(user: Annotated[User, Depends(authenticate_user)]):
    """
    Handles getting token process
    """
    token = generate_token(payload=Payload(user_id=str(user.id), email=user.email))
    return Token(token=token)
