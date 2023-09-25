from datetime import datetime

from app.schemas.token import Payload
from app.database.models.user import User
from app.database.managers import UserManager
from app.database.connect import get_session
from app.exeptions import client_exception, client_schemes


async def verify_token_email(email: str) -> User:
    """
    Check if there is an email in the database
    return user
    """
    async with get_session() as session:
        database = UserManager(session)
        user: User = await database.get_user_by_email(email)
    if not user:
        raise client_exception.TokenException(
            status_code=401,
            detail=client_schemes.TokenExeptionScheme(
                code=401, message="You token is invalid"
            ),
        )
    return user


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
        raise client_exception.TokenException(
            status_code=401,
            detail=client_schemes.TokenExeptionScheme(
                code=401, message="You token is invalid"
            ),
        )
    return verify_payload
