from app.schemas.user import UserLogin, UserAuth
from app.database.db import Database
from app.utils.helpers import verify_password
from app.database.models.user import User
from app.database.db import Database
from app.settings.config import TokenSettings

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
    payload = jwt.decode(token=token, key=TokenSettings().TOKEN_KEY, algorithms=TokenSettings().TOKEN_ALGORITHM)
    return payload


async def get_current_user_from_token_payload(payload: Annotated[dict, Depends(get_token_payload)]):
    user_id = payload.get("user_id")
    email = payload.get("email")
    exp = payload.get("exp")
    return (user_id, email, exp)