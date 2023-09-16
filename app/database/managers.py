from app.database.db import Database
from app.schemas.user import UserAuth, UserUpdate
from app.database.models.user import User
from app.database.models.product import Product
from app.serializers.user import UserSerializer

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import UUID, select


class ProductManager(Database):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)


    async def get_products(self, limit, offset) -> list[Product]:
        query = select(Product).offset(offset).limit(limit)
        result = await self.session.execute(query)
        products = result.scalars().all()
        return products


class UserManager(Database):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)


    async def get_user_by_email(self, email) -> User:
        """
        Accepts validated email and looks up the user in the database
        """
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        user = result.scalars().first()
        return user


    async def get_user_by_username(self, username) -> User:
        """
        Accept username from request, and look up user in the database
        """
        query = select(User).where(User.username == username)
        result = await self.session.execute(query)
        user = result.scalars().first()
        return user


    async def get_users_from_db(self, limit, offset) -> list[User]:
        """
        Accept request params: limit - quantity result, offset - start from
        Return all users[offset: offset+limit]
        """
        query = select(User).offset(offset).limit(limit)
        result = await self.session.execute(query)
        users = result.scalars().all()
        return users


    async def create_user_in_db(self, user: UserAuth) -> UUID:
        """
        Create new user in the database
        Return UUID the user
        """
        user_serialization = UserSerializer(user.model_dump()).to_save_in_db()
        new_user = User(**user_serialization)
        self.session.add(new_user)
        return new_user



    async def update_user(self, user: User, data: UserUpdate) -> None:
        """
        Accept user - current user and data - json data from request according to UserUpdate schema
        """
        if data.username:
            user.username = data.username
        if data.email:
            user.email = data.email
        self.session.add(user)

    async def delete_account(self, user: User) -> None:
        await self.session.delete(user)
