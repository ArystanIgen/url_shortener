import pytest_asyncio
from typing import Generator
from datetime import datetime
from app.repositories import LinkRepository
from app.schemas import LinkIn, LinkCreate
from app.models import LinkModel
from app.services.utils import set_end_date
from sqlalchemy.ext.asyncio import AsyncSession


@pytest_asyncio.fixture(scope="function")
async def test_created_shortened_link(
        async_session: AsyncSession,
        mock_shortened_link: LinkIn
) -> Generator[LinkModel, None, None]:
    link_repo = LinkRepository()
    link_create = LinkCreate(
        **mock_shortened_link.dict(),
        end_date=set_end_date(
            date_quantity=mock_shortened_link.date_quantity,
            date_category=mock_shortened_link.date_category
        )

    )
    link_instance: LinkModel = await link_repo.create_shortened_link(
        async_session=async_session,
        link=link_create
    )

    yield link_instance
    await link_repo.remove(async_session=async_session, id_=link_instance.id)


@pytest_asyncio.fixture(scope="function")
async def test_created_shortened_link_expired(
        async_session: AsyncSession,
        mock_shortened_link: LinkIn
) -> Generator[LinkModel, None, None]:
    link_repo = LinkRepository()
    link_create = LinkCreate(
        **mock_shortened_link.dict(),
        end_date=datetime.utcnow()
    )
    link_instance: LinkModel = await link_repo.create_shortened_link(
        async_session=async_session,
        link=link_create
    )

    yield link_instance
    await link_repo.remove(async_session=async_session, id_=link_instance.id)