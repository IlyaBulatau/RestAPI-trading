from app.utils.helpers import hashed_password
from app.schemas.user import UserInfo
from app.database.models.user import User

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
    
    def responce_user_info(self) -> UserInfo:
        """
        serialize database user model to schema UserInfo
        """
        self.data: User
        create_on = self.data.created_on.strftime("%A, %B %d, %Y %I:%M:%S")
        return UserInfo(email=self.data.email, 
                        username=self.data.username, 
                        create_on=create_on,)