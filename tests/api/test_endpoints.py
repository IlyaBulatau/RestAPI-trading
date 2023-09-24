from fastapi.testclient import TestClient

from app.settings.constance import AUTH_ROUTE_URI
from app.schemas.user import UserAuth


class TestUserAuthHandler:
    
    username = "Test"
    email = "test@gmail.com"
    password = "testtest123321$$!"

    async def test_signup_handler(self, client: TestClient):
        user = UserAuth(
            username=self.username,
            email=self.email,
            password=self.password
        )
        response = client.post(AUTH_ROUTE_URI+"/signup", data=user.model_dump_json())
        print(response.json())


class TestUserHandler:
    ...


class TestProductHandler:
    ...
