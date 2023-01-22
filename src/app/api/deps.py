from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import BaseModel as DBBaseModel
from app.db.session import async_session
from app.repositories import LinkRepository

ModelType = TypeVar('ModelType', bound=DBBaseModel)


async def get_session() -> AsyncSession:
    try:
        yield async_session
    except Exception as e:
        print(e)
        await async_session.rollback()
    finally:
        await async_session.close()


def get_link_repo() -> LinkRepository:
    return LinkRepository()
