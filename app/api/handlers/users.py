from app.database.models.user import User
from app.auth.actions import get_current_user
from app.schemas.user import UserResponseInfo, UserList, UserUpdate
from app.database.db import Database
from app.database.connect import get_session
from app.settings.constance import USER_ROUTE_URI
from app.servise.dependens import GET_CURRENT_USER, VALIDATE_USERNAME_REGULAR

from fastapi import APIRouter, Depends, HTTPException, status, Query

from typing import Annotated


router = APIRouter(
    prefix=USER_ROUTE_URI, tags=["users"], dependencies=[Depends(get_current_user)]
)


@router.get(
    path="/me",
    response_model=UserResponseInfo,
    status_code=200,
    response_description="Return user info by bearer token",
)
async def get_me_info(current_user: GET_CURRENT_USER):
    return UserResponseInfo(
        email=current_user.email,
        username=current_user.username,
        create_on=current_user.created_on,
    )


@router.get(
    path="/{username}",
    status_code=200,
    response_model=UserResponseInfo,
    response_description="Return user info by path param username",
)
async def get_user_by_username(username: VALIDATE_USERNAME_REGULAR):
    # try get user
    async with get_session() as session:
        database = Database(session)
        user = await database.get_user_by_username(username=username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Page Not Found"
        )
    return UserResponseInfo(
        email=user.email, username=user.username, create_on=user.created_on
    )


@router.get(
    path="/",
    status_code=200,
    response_model=UserList,
    response_description="Return list of users start from 'offset' in the number of 'limit'",
)
async def get_all_users(
    limit: Annotated[
        int, Query(ge=1, le=100, description="number of results to be returned")
    ] = 10,
    offset: Annotated[
        int, Query(ge=1, le=100000, description="starting from number")
    ] = 1,
):
    async with get_session() as session:
        database = Database(session)
        users: list[User] = await database.get_users_from_db(
            limit=limit, offset=offset - 1
        )

    return UserList(
        users=[
            UserResponseInfo(
                email=user.email, username=user.username, create_on=user.created_on
            )
            for user in users
        ]
    )


@router.put(
    path="/{username}/update",
    status_code=200,
    response_model=dict[str, str],
    response_description="Update user data and return successfull message",
)
async def update_user_data(
    current_user: GET_CURRENT_USER,
    data: UserUpdate,
    username: VALIDATE_USERNAME_REGULAR,
):
    # if the user doesn't current
    if username != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only change your account",
        )
    # if data is empty
    if not any([data.username, data.email]):
        return {"Message": "Data is empty"}

    async with get_session() as session:
        database = Database(session)
        await database.update_user(current_user, data)

    return {"Message": "Successfull update data"}


@router.delete(
    path="/{username}/delete", status_code=204, description="Delete account by username"
)
async def delete_user_by_username(
    current_user: Annotated[User, Depends(get_current_user)],
    username: VALIDATE_USERNAME_REGULAR,
):
    if current_user.username != username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your account",
        )
    async with get_session() as session:
        database = Database(session)
        await database.delete_account(current_user)
