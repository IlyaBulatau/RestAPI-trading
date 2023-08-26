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
        data_to_dict = dict(self.data)
        hash_password = hashed_password(data_to_dict.pop("password"))
        data_to_dict.update({"hash_password": hash_password})
        
        return data_to_dict 