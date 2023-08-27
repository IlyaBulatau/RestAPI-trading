from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from typing import Annotated

from app.schemas.user import UserAuth, UserResponce
from app.schemas.token import Token, Payload
from app.database import db
from app.database.models.user import User
from app.auth.actions import authenticate_user, is_exists_user
from app.utils.helpers import generate_token


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(path="/signup", 
            response_model=UserResponce, 
            status_code=201, 
            response_description="Responce userID, username and email")
async def signup_process(user: Annotated[UserAuth, Depends(is_exists_user)]):
    """
    Handles registration process
    """ 
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
    token = generate_token(payload=Payload(user_id=str(user.id), email=user.email))
    return Token(token=token)