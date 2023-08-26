from app.utils.helpers import hashed_password

from typing import Dict, Any

class UserSerializer:
    """
    serialize data for work with user
    """

    def __init__(self, data: Any):
        self.data = data

    def to_save_in_db(self) -> Dict[str, str]:
        """
        serialize user data before save in DB
        """
        return {
            "username": self.data.username,
            "email": self.data.email ,
            "hash_password": hashed_password(self.data.password)
        }