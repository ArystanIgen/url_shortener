from fastapi.testclient import TestClient


def test_redirect_with_status_303(
        client: TestClient) -> None:
    """
    The case when the redirect is successfull (303 status).
    """

    response = client.get(url="/kjdsfnsd")

    assert response.status_code == 303
