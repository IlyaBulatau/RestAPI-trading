from app.schemas.user import UserLogin, UserAuth
from app.database.db import Database
from app.utils.helpers import verify_password
from app.database.models.user import User
from app.database.db import Database
from app.settings.config import TokenSettings
from app.schemas.token import Payload

from datetime import datetime
from typing import Annotated

from jose import jwt
from fastapi.exceptions import HTTPException
from fastapi import status, Depends
from fastapi.security import OAuth2PasswordBearer


oauth_schema = OAuth2PasswordBearer("signin", scheme_name="get_token", description="get token from authorization headers")

async def authenticate_user(user: UserLogin) -> User:
    """
    The func conducts the authentication process
    """
    user_from_db = await Database().get_user_by_email(user.email)
    if not user_from_db:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You email not found")
    if not verify_password(password=user.password, hash_password=user_from_db.hash_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Password is invalid")
    return user_from_db
    
async def is_exists_user(user: UserAuth) -> bool:
    """
    Check exists user in database
    """
    user_from_db = await Database().get_user_by_email(user.email)
    if user_from_db:
        return True
    return False

async def get_token_payload(token: Annotated[str, Depends(oauth_schema)]):
    """
    Accept token from request header and decode in payload(dict), which contains user_id, email and exp keys
    """
    payload = jwt.decode(token=token, key=TokenSettings().TOKEN_KEY, algorithms=TokenSettings().TOKEN_ALGORITHM)
    return payload

async def verify_token_time(exp: datetime) -> bool:
    """
    Checking token time exp and compare with datetime now
    """
    if datetime.utcnow() > exp:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token time is up")

async def verify_token_email(email: str) -> User:
    """
    Check if there is an email in the database
    return user
    """
    user = await Database().get_user_by_email(email)
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You token is invalid")


async def verify_payload_from_token(payload: dict) -> Payload:
    """
    Check if payload compares to schema
    return Payload schema
    """
    # copy data
    copy_payload = payload.copy()
    # covert second to datetime
    copy_payload["exp"] = datetime.fromtimestamp(copy_payload["exp"])
    # create Payload object
    verify_payload = Payload(**copy_payload)

    if copy_payload != dict(verify_payload):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return verify_payload


async def get_current_user(payload: Annotated[dict, Depends(get_token_payload)]) -> User:
    """
    validate payload and return current user object from database
    """
    payload_schema = await verify_payload_from_token(payload)
    await verify_token_time(payload_schema.exp)
    user = await verify_token_email(payload_schema.email)
    return user

