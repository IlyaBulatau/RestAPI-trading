from typing import Annotated

from app.database.models.user import User
from app.auth.actions import get_current_user

from fastapi import Depends

GET_CURRENT_USER = Annotated[User, Depends(get_current_user)]