from app.schemas.user import UserLogin, UserAuth
from app.database.db import Database
from app.utils.helpers import verify_password
from app.database.models.user import User
from app.database.db import Database

async def authenticate_user(user: UserLogin) -> User:
    """
    The func conducts the authentication process
    """
    user_from_db = await Database().get_user_by_email(user.email)
    if not user_from_db:
        return False
    if not verify_password(password=user.password, hash_password=user_from_db.hash_password):
        return False
    return user_from_db
    
async def is_exists_user(user: UserAuth) -> bool:
    """
    Check exists user in database
    """
    user_from_db = await Database().get_user_by_email(user.email)
    if user_from_db:
        return True
    return False