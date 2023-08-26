from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from app.schemas.user import UserAuth, UserResponce, UserLogin
from app.database import db
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
        return JSONResponse(content={"Result": {"Status": 200, "User status": "Is exists"}})
    user_id = await db.Database().create_user_in_db(user)
    return UserResponce(username=user.username, email=user.email, id=user_id)

@router.post(path="/signin",  
            status_code=200,
            response_description="Responce token")
async def signin_process(user: UserLogin):
    """
    Handles getting token process
    """
    is_user = await authenticate_user(user)
    if not is_user:
        return JSONResponse(content={"Error": {"Invalid Data": "Check correct username and password", "Status": 401}}, 
                       status_code=status.HTTP_401_UNAUTHORIZED)
    
    token = generate_token(payload={"user_id": str(is_user.id), "email":is_user.email})
    return JSONResponse(content={"OK": {"token": token}}, 
                    status_code=status.HTTP_200_OK)
    