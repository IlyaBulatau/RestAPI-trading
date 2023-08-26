from passlib.hash import pbkdf2_sha256


def hashed_password(password: str) -> str:
    """
    Hashed password for save in database
    """
    hash_password = pbkdf2_sha256.hash(password)
    return hash_password

def verify_password(password: str, hash_password: str) -> bool:
    """
    Verify password from user json data with hash_password from database
    """
    return pbkdf2_sha256.verify(password, hash_password)
    

