
from fastapi.testclient import TestClient


def test_create_shortened_link_with_status_201(
        client: TestClient,
        mock_original_link: str) -> None:
    """
    The case when the shortened link is successfully created (201 status).
    """
    response = client.post(
        url="/v1/link", json={
            "original_link": mock_original_link,
            "date_category": "DAY",
            "date_quantity": 70

        }
    )

    assert response.status_code == 201

    data = response.json()
    assert "shortened_link" in data
    assert "end_date" in data
    assert "original_link" in data


