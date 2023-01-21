import logging

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_link_repo, get_session
from app.models import LinkModel
from app.repositories import LinkRepository
from app.schemas import LinkCreate, LinkIn, LinkOut
from app.services.utils import set_end_date

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    '',
    response_model=LinkOut,
    status_code=status.HTTP_201_CREATED,
    summary='CreateShortenedLink',
    description='Создание нового сокращенной ссылки',
    operation_id='CreateShortenedLink',
    response_description='Сокращенная ссылка',
)
async def create_shortened_link(
    link_in: LinkIn,
    async_session: AsyncSession = Depends(get_session),
    link_repo: LinkRepository = Depends(get_link_repo),
) -> LinkModel:
    return await link_repo.create_shortened_link(
        async_session=async_session,
        link=LinkCreate(
            **link_in.dict(),
            end_date=set_end_date(
                date_quantity=link_in.date_quantity,
                date_category=link_in.date_category
            )
        )
    )
