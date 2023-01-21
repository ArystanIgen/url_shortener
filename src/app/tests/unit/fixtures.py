from pytest import fixture
from sqlalchemy.orm import Session
from typing import Generator
from app.schemas import LinkIn
from app.models import LinkModel
from app.services.utils import set_end_date


@fixture(scope='function')
def test_created_shortened_link(
        session: Session,
        mock_shortened_link: LinkIn
) -> Generator[LinkModel, None, None]:
    link_instance: LinkModel = LinkModel(
        **mock_shortened_link.dict(),
        end_date=set_end_date(
            date_quantity=mock_shortened_link.date_quantity,
            date_category=mock_shortened_link.date_category
        ))

    session.add(link_instance)
    session.commit()
    session.refresh(link_instance)

    yield link_instance
    print("DELETEEEEEEEEEEE")

    session.delete(link_instance)
    session.commit()
