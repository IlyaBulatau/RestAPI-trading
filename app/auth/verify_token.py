from datetime import datetime

from app.schemas.token import Payload
from app.database.models.user import User
from app.database.managers import UserManager
from app.database.connect import get_session

from fastapi import status
from fastapi.exceptions import HTTPException


async def verify_token_time(exp: datetime) -> None:
    """
    Checking token time exp and compare with datetime now
    """
    if datetime.utcnow() > exp:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token time is up"
        )


async def verify_token_email(email: str) -> User:
    """
    Check if there is an email in the database
    return user
    """
    async with get_session() as session:
        database = UserManager(session)
        user: User = await database.get_user_by_email(email)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="You token is invalid"
    )


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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    return verify_payload
