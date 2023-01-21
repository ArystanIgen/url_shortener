import logging
from typing import Generic, List, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession


from app.db.base import BaseModel as DBBaseModel

logger = logging.getLogger(__name__)

ModelType = TypeVar('ModelType', bound=DBBaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    CRUD object with default methods to Create, Read, Update, Delete (CRUD).
    * `model`: A SQLAlchemy model class
    """
    model: Type[ModelType]

    async def get_multi(
        self,
        async_session: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[ModelType]:  # pragma: no cover
        stmt = select(self.model).order_by(self.model.id).offset(skip).limit(limit)
        query = await async_session.execute(stmt)
        return query.scalars.all()

    async def create(
        self,
        async_session: AsyncSession,
        *,
        obj_in: CreateSchemaType
    ) -> Optional[ModelType]:  # noqa # pragma: no cover
        try:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = self.model(**obj_in_data)  # type: ignore
            async_session.add(db_obj)
            await async_session.commit()
            await async_session.refresh(db_obj)
            return db_obj
        except Exception as e:
            logger.error(e)
            await async_session.rollback()
            raise

    async def update(
        self,
        async_session: AsyncSession,
        *,
        instance: ModelType,
        obj_update: UpdateSchemaType
    ) -> Optional[ModelType]:  # pragma: no cover
        update_data = obj_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(instance, key, value) if value else None
        await async_session.commit()
        return instance

    async def remove(
        self,
        async_session: AsyncSession,
        *,
        id_: int
    ) -> Optional[ModelType]:  # pragma: no cover
        query = delete(self.model).where(self.model.id == id_)
        await async_session.execute(query)
        return None
