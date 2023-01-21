from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# App Imports
from app.core.config import CONFIG

engine = create_engine(CONFIG.db.url, pool_pre_ping=True)
SessionMaker = sessionmaker(autoflush=False, autocommit=False, bind=engine)


def get_session() -> Iterator[Session]:
    session: Session = SessionMaker()
    try:
        yield session
    finally:
        session.close()
