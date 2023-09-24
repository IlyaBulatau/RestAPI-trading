from app.database.managers import ProductManager, UserManager
from app.schemas.user import UserAuth
from app.database.models.user import User


class TestUserCRUD:
    async def test_create_user(self, session):
        user = UserAuth(
            username="Root", password="roooot7891$!", email="root@gmail.com"
        )
        db = UserManager(session)
        new_user = await db.create_user_in_db(user)
        assert type(new_user) == User


class TestProductCRUD:
    ...
