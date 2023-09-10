from typing import Annotated

from app.database.models.user import User
from app.auth.actions import get_current_user
from app.database.connect import get_session

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Path


GET_CURRENT_USER = Annotated[User, Depends(get_current_user)]
VALIDATE_USERNAME_REGULAR = Annotated[
    str, Path(pattern=r"^[a-zA-Z0-9]+([_ -]?[a-zA-Z0-9])*$")
]
GET_SESSION = Annotated[AsyncSession, Depends(get_session)]
