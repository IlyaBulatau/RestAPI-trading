from fastapi import APIRouter, Depends, HTTPException, status

from typing import Annotated

from app.schemas.user import UserAuthResponse, UserAuth
from app.schemas.token import Token, Payload
from app.database import db
from app.database.models.user import User
from app.auth.actions import authenticate_user, is_exists_user
from app.utils.helpers import generate_token
from app.settings.constance import AUTH_ROUTE_URI


router = APIRouter(prefix=AUTH_ROUTE_URI, tags=["auth"])


@router.post(
    path="/signup",
    response_model=UserAuthResponse,
    status_code=201,
    response_description="Responce userID, username and email",
)
async def signup_process(user: UserAuth):
    """
    Handles registration process
    :user - user model form Database
    :links - list links(LinkResponse objects) for payload generated
    """
    if await is_exists_user(user):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="with the email or username user is exist",
        )
    new_user: User = await db.Database().create_user_in_db(user)
    user_with_id = await db.Database().get_user_by_email(new_user.email)
    return UserAuthResponse(
        id=user_with_id.id,
        email=new_user.email,
        username=new_user.username,
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
