from abc import ABC

from app.database.models.user import User

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import UUID, select


class Database(ABC):
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def get_user_by_id(self, id: UUID) -> User:
        """
        Return user model from database by ID
        """
        query = select(User).where(User.id == id)
        result = await self.session.execute(query)
        user = result.scalars().first()
        return user
