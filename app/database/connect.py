from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from contextlib import asynccontextmanager

from app.settings.config import DataBaseSettings
from app.servise.bg_tasks.tasks import send_to_email_log


async_engine = create_async_engine(
    url=DataBaseSettings().get_url(), echo=DataBaseSettings().DB_ECHO, future=True
)
async_session = async_sessionmaker(
    bind=async_engine, expire_on_commit=False, class_=AsyncSession
)


@asynccontextmanager
async def get_session() -> AsyncSession:
    """
    opens a session to work with transactions
    if an exception occurs rolls back changes
    after work with transactions has stopped closes the session
    """
    session = async_session()
    try:
        yield session
        await session.commit()
    except Exception as e:
        await session.rollback()
        send_to_email_log.delay(f"DATABASE EXCEPTION:\n{str(e)}")
    finally:
        await session.close()
