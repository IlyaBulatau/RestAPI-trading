from app.schemas.user import UserLogin, UserAuth
from app.database.db import Database
from app.utils.helpers import verify_password
from app.database.models.user import User
from app.database.db import Database
from app.settings.config import TokenSettings
from app.auth.verify_token import (
    verify_payload_from_token,
    verify_token_email,
    verify_token_time,
)
from app.exeptions.http.responses import ResponseGenerator
from app.exeptions.http import response_text as RT

from typing import Annotated

from jose import jwt
from jose.exceptions import ExpiredSignatureError
from fastapi.exceptions import HTTPException
from fastapi import status, Depends
from fastapi.security import OAuth2PasswordBearer


oauth_schema = OAuth2PasswordBearer(
    "signin",
    scheme_name="get_token",
    description="get token from authorization headers",
)


async def authenticate_user(user: UserLogin) -> User:
    """
    The func conducts the authentication process
    """
    user_from_db = await Database().get_user_by_email(user.email)
    # if user not found in database
    if not user_from_db:
        # generate error response
        status_code = status.HTTP_401_UNAUTHORIZED
        response = ResponseGenerator(
            user.email,
            title=RT.TITLE_EMAIL_EXEPTION,
            status_code=status_code,
            descriptions=("email", RT.TEXT_EMAIL_NOT_FOUND),
        ).generate_response()

        raise HTTPException(status_code=status_code, detail=response)
    # password invalid
    if not verify_password(
        password=user.password, hash_password=user_from_db.hash_password
    ):
        # generate error response
        status_code = status.HTTP_401_UNAUTHORIZED
        response = ResponseGenerator(
            title=RT.TITLE_PASSWORD_EXEPTION,
            status_code=status_code,
            descriptions=("password", RT.TEXT_PASSWORD_INVALID),
        ).generate_response()

        raise HTTPException(status_code=status_code, detail=response)
    return user_from_db


async def is_exists_user(user: UserAuth) -> bool:
    """
    Check exists user in database
    if user in database - raise exeption else return user to create new
    """
    user_from_db_by_email = await Database().get_user_by_email(user.email)
    user_from_db_by_username = await Database().get_user_by_username(user.username)
    if any([user_from_db_by_email, user_from_db_by_username]):
        return True
    return False


async def get_token_payload(token: Annotated[str, Depends(oauth_schema)]):
    """
    Accept token from request header and decode in payload(dict), which contains user_id, email and exp keys
    """
    try:
        payload = jwt.decode(
            token=token,
            key=TokenSettings().TOKEN_KEY,
            algorithms=TokenSettings().TOKEN_ALGORITHM,
        )
        return payload
    except ExpiredSignatureError as e:
        status_code = status.HTTP_401_UNAUTHORIZED
        response = ResponseGenerator(
            title=RT.TITLE_TOKEN_EXEPTION,
            status_code=status_code,
            descriptions=("token", RT.TEXT_TOKEN_EXPIRED),
        ).generate_response()
        raise HTTPException(status_code=status_code, detail=response)


async def get_current_user(
    payload: Annotated[dict, Depends(get_token_payload)]
) -> User:
    """
    validate payload and return current user object from database
    """
    payload_schema = await verify_payload_from_token(payload)
    await verify_token_time(payload_schema.exp)
    user = await verify_token_email(payload_schema.email)
    return user
