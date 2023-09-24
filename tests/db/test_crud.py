from app.database.managers import ProductManager, UserManager
from app.schemas.user import UserAuth
from app.database.models.user import User
from app.utils.helpers import verify_password

import uuid


class TestUserCRUD:

    username = "Root"
    password = "roooot7891$!"
    email = "root@gmail.com"

    async def test_create_user(self, session):
        user = UserAuth(
            username=self.username, password=self.password, email=self.email
        )
        db = UserManager(session)
        new_user = await db.create_user_in_db(user)
        assert type(new_user) == User
        assert new_user.username == self.username
        assert verify_password(self.password, new_user.hash_password) == True

    async def test_get_user_by_id(self):
        ...


class TestProductCRUD:
    ...
