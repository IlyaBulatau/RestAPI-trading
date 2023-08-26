from app.schemas.user import UserAuth
from app.database.connect import get_session
from app.database.models.user import User
from app.serializers.user import UserSerializer
from app.database.models.user import User

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import UUID, select


class Database:

    async def create_user_in_db(self, user: UserAuth) -> UUID:
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
    
    async def get_user_by_email(self, email) -> User:
        """
        Accepts validated email and looks up the user in the database
        """
        query = select(User).where(User.email == email)
        async  with get_session() as session:
            session: AsyncSession
            result = await session.execute(query)
            user = result.scalars().first()
        return user

        

