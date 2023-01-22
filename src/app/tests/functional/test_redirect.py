import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import LinkModel


@pytest.mark.asyncio
async def test_redirect_with_status_303(
        async_client: AsyncClient,
        test_created_shortened_link: LinkModel
):
    response = await async_client.get(f"/{test_created_shortened_link.uuid}")

    assert response.status_code == 303


@pytest.mark.asyncio
async def test_redirect_with_status_404(
        async_client: AsyncClient
):
    response = await async_client.get("/1234567890")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_redirect_with_status_403(
        async_client: AsyncClient,
        test_created_shortened_link_expired: LinkModel,
):
    response = await async_client.get(f"/{test_created_shortened_link_expired.uuid}")

    assert response.status_code == 403
