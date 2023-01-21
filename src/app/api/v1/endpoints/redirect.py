# Standard Library
import logging
from datetime import datetime
from fastapi import (
    Depends,
    APIRouter,
    status
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import (
    get_session,
    get_link_repo,
)
# App Imports
from app.exceptions import LinkExpiredError,LinkNotFoundError
from app.models import LinkModel
from app.repositories import LinkRepository
from starlette.responses import RedirectResponse


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    '/{link_id}',
    summary='CreateShortenedLink',
    description='Создание нового сокращенной ссылки',
    operation_id='CreateShortenedLink',
    include_in_schema=False
)
async def redirect_to_original_link(
    link_id: str,
    async_session: AsyncSession = Depends(get_session),
    link_repo: LinkRepository = Depends(get_link_repo),
) -> RedirectResponse:
    fetched_link: LinkModel = await link_repo.get_by_uuid(async_session=async_session, uuid_=link_id)

    if datetime.utcnow() >= fetched_link.end_date:
        raise LinkExpiredError

    return RedirectResponse(
        url=fetched_link.original_link,
        status_code=status.HTTP_303_SEE_OTHER
    )
