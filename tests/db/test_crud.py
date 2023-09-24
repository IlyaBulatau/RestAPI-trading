from app.database.managers import ProductManager, UserManager
from app.database.models import User, Product
from app.schemas.user import UserAuth, UserUpdate
from app.database.models.user import User
from app.utils.helpers import verify_password


class TestUserCRUD:

    username = "Root"
    password = "roooot7891$!"
    email = "root@gmail.com"

    async def test_create_user(self, session):
        user = UserAuth(
            username=self.username, password=self.password, email=self.email
        )
        db = UserManager(session)
        new_user: User = await db.create_user_in_db(user)
        TestUserCRUD.id = new_user.id
        assert type(new_user) == User
        assert new_user.username == self.username
        assert new_user.email == self.email
        assert verify_password(self.password, new_user.hash_password) == True


    async def test_get_user_by_id(self, session):
        db = UserManager(session)

        user: User = await db.get_user_by_id(self.id)
        assert type(user) == User
        assert user.id == self.id
        assert user.email == self.email
        assert user.username == self.username


    async def test_get_user_by_username(self, session):
        db = UserManager(session)

        user: User = await db.get_user_by_username(self.username)
        assert type(user) == User
        assert user.id == self.id
        assert user.username == self.username
        assert user.email == self.email


    async def test_update_user(self, session):
        db = UserManager(session)

        user: User = await db.get_user_by_email(self.email)
        assert type(user) == User
        data = UserUpdate(
            username="Root2"
        )
        await db.update_user(user, data)


class TestProductCRUD:
    ...
