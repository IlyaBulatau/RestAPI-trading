from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from typing import Annotated

from app.schemas.user import UserAuth, UserResponce, UserLogin
from app.schemas.token import Token
from app.database import db
from app.database.models.user import User
from app.auth.actions import authenticate_user, is_exists_user
from app.utils.helpers import generate_token


router = APIRouter(prefix="/auth", tags=["auth"])
oauth_schema = OAuth2PasswordBearer("signin", scheme_name="get_token", description="get token from headers")


@router.post(path="/signup", 
            response_model=UserResponce, 
            status_code=201, 
            response_description="Responce userID, username and email")
async def signup_process(user: UserAuth):
    """
    Handles registration process
    """
    if is_exists_user(user):
        return JSONResponse(content={"Result": {"Status": 200, "Operation": "Not exists, this is user is exists"}})
    user_id = await db.Database().create_user_in_db(user)
    return UserResponce(username=user.username, email=user.email, id=user_id)

@router.post(path="/signin",  
            status_code=200,
            response_model=Token,
            response_description="Responce token")
async def signin_process(user: Annotated[User, Depends(authenticate_user)]):
    """
    Handles getting token process
    """
    if not user:
        return JSONResponse(content={"Error": {"Invalid Data": "Check correct username and password", "Status": 401}}, 
                       status_code=status.HTTP_401_UNAUTHORIZED)
    
    token = generate_token(payload={"user_id": str(user.id), "email":user.email})
    return Token(token=token)