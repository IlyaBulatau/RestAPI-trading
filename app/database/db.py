from app.schemas.user import UserAuth
from app.database.connect import get_session
from app.database.models.user import User
from app.serializers.user import UserSerializer

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import UUID


class Database:

    async def create_user_in_db(sef, user: UserAuth) -> UUID:
        """
        Create new user in the database
        Return UUID the user 
        """
        user_data = UserSerializer(user).to_save_in_db()
        save_user = User(**user_data)
        async with get_session() as session:
            session: AsyncSession
            session.add(save_user)
        return save_user.id
        

