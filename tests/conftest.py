from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
)
import pytest
import asyncpg
from fastapi.testclient import TestClient

import asyncio
from typing import Generator

from app.main import app
from app.database.models.base import Base
from app.settings.config import DataBaseSettings


db_settings = DataBaseSettings()
DB_NAME = "test_app"
DB_URL = f"postgresql+asyncpg://{db_settings.DB_LOGIN}:{db_settings.DB_PASSWORD}@{db_settings.DB_HOST}:{db_settings.DB_PORT}/{DB_NAME}"
client = TestClient(app)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.new_event_loop()
    try:
        yield loop
    finally:
        loop.close()


@pytest.fixture(scope="session")
async def database(event_loop) -> None:
    """
    Drop old database before testing, if its exists
    And create new database
    """
    conn: asyncpg.connection.Connection = await asyncpg.connect(
        database="postgres",
        user=db_settings.DB_LOGIN,
        password=db_settings.DB_PASSWORD,
        host=db_settings.DB_HOST,
        port=db_settings.DB_PORT,
    )

    query: str = (
        f"SELECT datname FROM pg_catalog.pg_database WHERE datname = '{DB_NAME}'"
    )
    database_search: str = await conn.execute(query)

    if not database_search == "SELECT 0":
        await conn.execute(f"DROP DATABASE {DB_NAME};")

    await conn.execute(f"CREATE DATABASE {DB_NAME};")
    await conn.close()


@pytest.fixture(scope="session")
def engine(event_loop) -> AsyncEngine:
    e = create_async_engine(
        url=DB_URL,
        future=True,
    )
    yield e


@pytest.fixture(scope="session")
def create_session(engine, event_loop):
    a_s = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
    yield a_s


@pytest.fixture(scope="session")
async def create_table(engine: AsyncEngine, event_loop) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="function")
async def session(database, create_table, create_session) -> AsyncSession:
    async with create_session() as new_session:
        yield new_session
        await new_session.commit()
        await new_session.close()


@pytest.fixture(scope="function")
async def client(create_session) -> TestClient:
    cl = TestClient(app)
    yield cl