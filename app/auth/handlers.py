from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer

from app.schemas.user import UserAuth, UserResponce, UserLogin
from app.database import db


router = APIRouter(prefix="/auth", tags=["auth"])
oauth_schema = OAuth2PasswordBearer("signin", scheme_name="get_token", description="get token from headers")


@router.post(path="/signup", response_model=UserResponce, status_code=201)
async def signup_process(user: UserAuth):
    """
    Handles registration process
    """
    user_id = await db.Database().create_user_in_db(user)
    return UserResponce(login=user.username, email=user.email, id=user_id)

@router.post(path="/signin")
async def signin_process(user: UserLogin):
    """
    Handles getting token process
    """
    ...
    