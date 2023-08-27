from app.database.models.user import User
from app.auth.actions import get_current_user
from app.schemas.user import UserInfo
from app.serializers.user import UserSerializer

from fastapi import APIRouter, Depends

from typing import Annotated


router = APIRouter(prefix="/v1/api", tags=["api"])


@router.get("/me", 
            response_model=UserInfo,
            status_code=200,
            response_description="Return user info by bearer token")
async def get_me_info(current_user: Annotated[User, Depends(get_current_user)]):
    return UserSerializer(current_user).responce_user_info()