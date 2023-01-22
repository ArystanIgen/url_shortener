import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_create_shortened_link_with_status_201(
        async_client: AsyncClient,
        mock_original_link: str
):
    response = await async_client.post("/v1/link", json={
            "original_link": mock_original_link,
            "date_category": "DAY",
            "date_quantity": 70
        })

    assert response.status_code == 201

    data = response.json()
    assert "shortened_link" in data
    assert "end_date" in data
    assert "original_link" in data
