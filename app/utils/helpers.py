from passlib.hash import pbkdf2_sha256
from jose import jwt

from datetime import datetime, timedelta

from app.settings.config import TokenSettings

def hashed_password(password: str) -> str:
    """
    Hashed password for save in database
    """
    hash_password = pbkdf2_sha256.hash(password)
    return hash_password

def verify_password(password: str, hash_password: str) -> bool:
    """
    Verify password from user json data with hash_password from database
    :payload = str(user_id) + email + exp
    """
    return pbkdf2_sha256.verify(password, hash_password)
    
def generate_token(payload: dict, exp: datetime = None):
    if not exp:
        expire = datetime.now() + timedelta(minutes=int(TokenSettings().TOKEN_LIMIT_MINUTES))
    else:
        expire = datetime.now() + exp
    payload.update({"exp": expire})
    token = jwt.encode(payload, 
                       key=TokenSettings().TOKEN_KEY, 
                       algorithm=TokenSettings().TOKEN_ALGORITHM)
    return token