from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from contextlib import asynccontextmanager

from app.settings.config import DataBaseSettings


async_engine = create_async_engine(
    url=DataBaseSettings().get_url(), echo=True, future=True
)
async_session = async_sessionmaker(
    bind=async_engine, expire_on_commit=False, class_=AsyncSession
)


@asynccontextmanager
async def get_session() -> AsyncSession:
    session = async_session()
    try:
        yield session
        await session.commit()
    except:
        await session.rollback()
    finally:
        await session.close()
