from app.database.db import Database
from app.schemas.user import UserAuth, UserUpdate
from app.database.models.user import User
from app.database.models.product import Product
from app.serializers.user import UserSerializer

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import UUID, select, insert
from sqlalchemy import orm


class ProductManager(Database):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def get_products(self, limit, offset) -> list[Product]:
        """
        Get all product from database
        Accept:
        :limit - how many object need to be taken
        :offset - starting from
        """
        query = (
            select(Product)
            .options(orm.joinedload(Product.owner))
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(query)
        products: list[Product] | None = result.scalars().all()
        return products

    async def get_product_by_id(self, product_id: int) -> Product:
        """
        Accept ID the product
        Search the product obj with its owner obj in the database
        Return Product obj
        """
        query = (
            select(Product)
            .options(orm.joinedload(Product.owner))
            .where(Product.id == product_id)
        )
        result = await self.session.execute(query)
        product: Product | None = result.scalars().first()
        return product

    async def create_product(self, dict_schema: dict, owner: User) -> Product:
        """
        Accept:
        :dict_scema - converted from Product schemas to dict obj
        :owner User model from database
        Insert in database product and return new product obj
        """
        query = (
            insert(Product)
            .values(
                title=dict_schema["title"],
                description=dict_schema["description"],
                price=dict_schema["price"],
                user_id=owner.id,
            )
            .returning(Product)
        )

        result = await self.session.execute(query)
        product = result.scalars().first()
        return product

    async def get_product_by_user_id(
        self, user_id: UUID, limit: int, offset: int
    ) -> list[Product]:
        """
        Accept user ID
        Return all products the user
        """
        query = (
            select(Product)
            .where(Product.user_id == user_id)
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(query)
        products: list[Product] | None = result.scalars().all()
        return products

    @staticmethod
    def model_dump(database_model: Product):
        """
        Converted Product model from database to Dict
        """
        return {
            "id": database_model.id,
            "title": database_model.title,
            "description": database_model.description,
            "price": database_model.price,
            "created_on": database_model.created_on,
        }


class UserManager(Database):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def get_user_by_email(self, email) -> User:
        """
        Accepts validated email and looks up the user in the database
        """
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        user: User | None = result.scalars().first()
        return user

    async def get_users_from_db(self, limit, offset) -> list[User]:
        """
        Accept request params: limit - quantity result, offset - start from
        Return all users[offset: offset+limit]
        """
        query = select(User).offset(offset).limit(limit)
        result = await self.session.execute(query)
        users: list[User] | None = result.scalars().all()
        return users

    async def create_user_in_db(self, user: UserAuth) -> User:
        """
        Create new user in the database
        Return User
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
