import asyncio

from typing import Generator, Iterator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy_utils import drop_database, create_database, database_exists
from sqlalchemy.engine import Engine
from app.api.deps import get_session

from app.db.base import BaseModel
from app.core.config import CONFIG
from app.main import main_app
from app.tests.functional.fixtures import *  # noqa
from app.tests.unit.fixtures import *  # noqa


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:  # noqa: indirect usage
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def async_session() -> AsyncSession:
    test_sync_db_url = f"postgresql://{CONFIG.db.username}:{CONFIG.db.password}@{CONFIG.db.host}:{CONFIG.db.port}/test"

    test_db_url = f"postgresql+asyncpg://{CONFIG.db.username}:{CONFIG.db.password}@{CONFIG.db.host}:{CONFIG.db.port}/test"

    if not database_exists(test_sync_db_url):
        create_database(test_sync_db_url)

    test_async_engine = create_async_engine(url=test_db_url)

    session = sessionmaker(
        test_async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with session() as s:
        async with test_async_engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.create_all)

        yield s

    async with test_async_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)

    await test_async_engine.dispose()
    drop_database(test_sync_db_url)


@pytest_asyncio.fixture
async def async_client(async_session: Iterator[AsyncSession]):
    def _get_db_override() -> Iterator[AsyncSession]:
        return async_session  # pragma: no cover

    main_app.dependency_overrides[get_session] = _get_db_override

    async with AsyncClient(
            app=main_app,
            base_url=CONFIG.api.host
    ) as client:
        yield client
