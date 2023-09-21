from app.schemas.user import UserLogin, UserAuth
from app.schemas.token import Payload
from app.utils.helpers import verify_password
from app.database.models.user import User
from app.database.managers import UserManager
from app.settings.config import TokenSettings
from app.database.connect import get_session
from app.exeptions import client_exception, client_schemes
from app.auth.verify_token import (
    verify_payload_from_token,
    verify_token_email,
)

from typing import Annotated

from jose import jwt
from jose.exceptions import ExpiredSignatureError
from fastapi.exceptions import HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer


oauth_schema = OAuth2PasswordBearer(
    "signin",
    scheme_name="get_token",
    description="get token from authorization headers",
)


async def authenticate_user(user: UserLogin) -> User:
    """
    The func conducts the authentication process
    user: Pydantic model
    Search for user accourding data, and if user is found returns it,
    else raise Error
    """
    async with get_session() as session:
        database = UserManager(session)
        user_from_db: User = await database.get_user_by_email(user.email)
    # if user not found in database
    if not user_from_db:
        raise client_exception.AuthException(
            status_code=401,
            detail=client_schemes.AuthExceptionScheme(
                code=401, message=f"User with email {user.email} not found"
            ).model_dump(),
        )
    # password invalid
    if not verify_password(
        password=user.password, hash_password=user_from_db.hash_password
    ):
        raise client_exception.AuthException(
            status_code=401,
            detail=client_schemes.AuthExceptionScheme(
                code=401,
                message="Invalid Password",
            ).model_dump(),
        )
    return user_from_db


async def is_exists_user(user: UserAuth) -> bool:
    """
    Check exists user in database
    if user in database - raise exeption else return user to create new
    """
    async with get_session() as session:
        database = UserManager(session)
        user_from_db_by_email: User = await database.get_user_by_email(user.email)
        user_from_db_by_username: User = await database.get_user_by_username(
            user.username
        )
    # if username or email found in database - the user is exists
    if any([user_from_db_by_email, user_from_db_by_username]):
        return True
    return False


async def get_token_payload(token: Annotated[str, Depends(oauth_schema)]):
    """
    Accept token from request header and decode in payload(dict),
    which contains user_id, email and exp keys
    """
    try:
        payload = jwt.decode(
            token=token,
            key=TokenSettings().TOKEN_KEY,
            algorithms=TokenSettings().TOKEN_ALGORITHM,
        )
        return payload
    except ExpiredSignatureError as e:
        raise client_exception.TokenException(
            status_code=401,
            detail=client_schemes.TokenExeptionScheme(
                code=401, message="You token is expired"
            ).model_dump(),
        )


async def get_current_user(
    payload: Annotated[dict, Depends(get_token_payload)]
) -> User:
    """
    Accept token
    validate payload from token and
    return current user object from database
    """
    payload_schema: Payload = await verify_payload_from_token(payload)
    user: User = await verify_token_email(payload_schema.email)
    return user
