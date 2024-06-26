import asyncio
from typing import AsyncGenerator
from httpx import ASGITransport, AsyncClient

import pytest
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from main import app
from db.models import Base
from db.config import settings
from db.db_helper import session_dep


DB_URL_TEST = settings.get_db_url_test
engine_test = create_async_engine(
    url=DB_URL_TEST,
    poolclass=NullPool,
)
session_factory_test = async_sessionmaker(bind=engine_test)


async def override_session_dep():
    async with session_factory_test() as session:
        yield session
        await session.close()


app.dependency_overrides[session_dep] = override_session_dep


@pytest.fixture(scope="session", autouse=True)
async def create_tables():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # async with engine_test.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
