from typing import Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


from app.exceptions import LinkNotFoundError
from app.models import LinkModel
from app.repositories.base import BaseRepository
from app.schemas import (
    LinkCreate,
    LinkUpdate,
)


class LinkRepository(
    BaseRepository[
        LinkModel, LinkCreate, LinkUpdate]):
    model = LinkModel

    async def create_shortened_link(
            self,
            async_session: AsyncSession,
            *,
            link: LinkCreate
    ) -> Optional[LinkModel]:
        link_instance: LinkModel = self.model(**link.dict())
        async_session.add(link_instance)
        await async_session.commit()
        await async_session.refresh(link_instance)
        return link_instance

    async def get_by_uuid(
        self,
        async_session: AsyncSession,
        *,
        uuid_: Any
    ) -> Optional[LinkModel]:  # noqa
        stmt = select(self.model).where(self.model.uuid == uuid_)
        query = await async_session.execute(stmt)
        query = query.scalar()
        if query is None:
            raise LinkNotFoundError
        return query
