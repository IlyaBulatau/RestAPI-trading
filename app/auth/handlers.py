from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer

from app.schemas.user import UserAuth


router = APIRouter(prefix="/auth", tags=["auth"])
oauth_schema = OAuth2PasswordBearer("signin", scheme_name="get_token", description="get token from headers")


@router.post(path="/signup", response_model=..., status_code=201)
async def signup_process(user: UserAuth):
    """
    Handles registration process
    """
    ...

@router.post(path="/signin")
async def signin_process():
    """
    Handles getting token process
    """
    ...