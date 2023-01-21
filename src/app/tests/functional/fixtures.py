from pytest import fixture
from app.schemas import LinkIn


@fixture(scope="function")
def mock_original_link() -> str:
    return "https://www.google.com/"


@fixture(scope="function")
def mock_shortened_link() -> LinkIn:
    return LinkIn(
        original_link="https://www.google.com/",
        date_category="DAY",
        date_quantity="70"
    )
