import asyncio

from typing import Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_engine
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


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(
            app=main_app,
            base_url=CONFIG.api.host
    ) as client:
        yield client


@pytest_asyncio.fixture(scope="function")
async def async_session() -> AsyncSession:
    session = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with session() as s:
        async with async_engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.create_all)

        yield s

    async with async_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)

    await async_engine.dispose()
