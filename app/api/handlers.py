from app.database.models.user import User
from app.auth.actions import get_current_user
from app.schemas.user import UserInfo
from app.serializers.user import UserSerializer
from app.database.db import Database

from fastapi import APIRouter, Depends, HTTPException, status, Query

from typing import Annotated


router = APIRouter(prefix="/v1/api/users", tags=["api"], dependencies=[Depends(get_current_user)])


@router.get("/me", 
            response_model=UserInfo,
            status_code=200,
            response_description="Return user info by bearer token")
async def get_me_info(current_user: Annotated[User, Depends(get_current_user)]):
    return UserSerializer(current_user).responce_user_info()


@router.get("/{username}")
async def get_user_by_username(username: str):
    user = await Database().get_user_by_username(username=username)
    if user:
        return UserSerializer(user).responce_user_info()
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Page Not Found")

@router.get("/",
            response_model=dict[str, list[UserInfo]])
async def get_all_users(limit: Annotated[int, Query(ge=1, 
                                                    le=10, 
                                                    description="number of results to be returned")] = 3,
                        offset: Annotated[int, Query(ge=1, 
                                                    le=100000,
                                                    description="starting from number")] = 1):
    users = await Database().get_users_from_db(limit=limit, offset=offset-1)
    serialize_users = UserSerializer(users).response_user_info_list()
    return {"Users": serialize_users}