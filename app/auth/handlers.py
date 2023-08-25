from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer


router = APIRouter(prefix="/auth", tags=["auth"])
oauth_schema = OAuth2PasswordBearer("signin", scheme_name="get_token", description="get token from headers")


@router.post(path="/signup", response_model=...)
async def signup_process():
    ...

@router.post(path="/signin")
async def signin_process():
    ...