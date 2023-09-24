from app.database.managers import ProductManager, UserManager
from app.database.models import User, Product
from app.schemas.user import UserAuth, UserUpdate
from app.schemas.product import ProductCreate
from app.database.models.user import User
from app.utils.helpers import verify_password


class TestUserCRUD:

    username = "Root"
    password = "roooot7891$!"
    email = "root@gmail.com"

    update_username = "Root2"

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
            username=self.update_username
        )
        await db.update_user(user, data)


class TestProductCRUD:

    title = "Product"
    description = "Cool product"
    price = 11.99
    
    async def test_create_product(self, session):
        db = ProductManager(session)

        owner: User = await db.get_user_by_username(TestUserCRUD.update_username)
        assert type(owner) == User
        product_sceme = ProductCreate(
            title=self.title,
            description=self.description,
            price=self.price
        )
        product: Product = await db.create_product(
            product_sceme.model_dump(),
            owner)
        
        assert type(product) == Product
        assert product.title == self.title
        assert product.description == self.description
        assert type(product.price) == float
        assert product.user_id == TestUserCRUD.id


    async def test_get_product_by_user_id(self, session):
        db = ProductManager(session)
        user_id = TestUserCRUD.id

        products: list[Product] = await db.get_product_by_user_id(user_id)
        assert type(products[0]) == Product
        assert products[0].title == self.title
        assert products[0].description == self.description
        assert type(products[0].price) == float


    async def test_get_all_products(self, session):
        db = ProductManager(session)

        products: list[Product] = await db.get_products()
        assert type(products[0]) == Product
        assert products[0].title == self.title
        assert products[0].description == self.description
        assert type(products[0].price) == float
