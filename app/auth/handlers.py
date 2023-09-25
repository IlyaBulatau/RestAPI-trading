from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Annotated

from app.servise.cache import cache_reset
from app.schemas.user import UserAuthResponse, UserAuth
from app.schemas.payload import PayloadForUser, Link
from app.schemas.token import Token, Payload
from app.database.managers import UserManager
from app.database.connect import get_session
from app.database.models.user import User
from app.auth.actions import authenticate_user, is_exists_user
from app.utils.helpers import generate_token
from app.settings.constance import AUTH_ROUTE_URI
from app.servise.bg_tasks.tasks import send_to_email_log


router = APIRouter(prefix=AUTH_ROUTE_URI, tags=["auth"])


@router.post(
    path="/signup",
    response_model=UserAuthResponse,
    status_code=201,
    response_description="Responce userID, username and email",
)
@cache_reset("get_all_users")
async def signup_process(user: UserAuth):
    """
    Handles registration process
    :user - user schemas
    """
    await is_exists_user(user)
    async with get_session() as session:
        database = UserManager(session)

        new_user: User = await database.create_user_in_db(user)

    send_to_email_log.delay(f"CREATE NEW USER WITH EMAIL: {new_user.email}")
    return UserAuthResponse(
        id=new_user.id,
        email=new_user.email,
        username=new_user.username,
        payload=PayloadForUser(
            links=[Link(detail="login path", href=AUTH_ROUTE_URI + "/login")]
        ),
    )


@router.post(
    path="/signin",
    status_code=200,
    response_model=Token,
    response_description="Responce token",
)
async def signin_process(user: Annotated[User, Depends(authenticate_user)]):
    """
    Checks if user is in database and
    Handles getting token process
    """
    token = generate_token(payload=Payload(user_id=str(user.id), email=user.email))
    return Token(token=token)
