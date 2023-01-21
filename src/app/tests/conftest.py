# Standard Library
from typing import Iterator

from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists, drop_database

from app.core.config import CONFIG
from app.db.base import BaseModel
# App Imports
from app.main import main_app
from app.tests.functional.fixtures import *  # noqa
from app.tests.test_db import get_session
from app.tests.unit.fixtures import *  # noqa


@fixture(scope="function")
def session() -> Iterator[Session]:
    db_engine = create_engine('sqlite:///./test.db', connect_args={'check_same_thread': False})
    connection = db_engine.connect()
    BaseModel.metadata.create_all(bind=db_engine)
    session = Session(bind=db_engine)
    yield session
    session.close()
    BaseModel.metadata.drop_all(bind=db_engine)
    connection.close()   # pragma: no cover


@fixture(scope="function")
def client(session: Iterator[Session]) -> TestClient:
    def _get_db_override() -> Iterator[Session]:
        return session  # pragma: no cover

    main_app.dependency_overrides[get_session] = _get_db_override
    return TestClient(main_app)
