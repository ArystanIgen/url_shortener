# Standard Library
import logging
from datetime import datetime

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

from app.api.deps import get_link_repo, get_session
# App Imports
from app.exceptions import LinkExpiredError
from app.models import LinkModel
from app.repositories import LinkRepository

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    '/{link_id}',
    summary='RedirectToOriginalLink',
    description='Перенаправление на оригнальную ссылку',
    operation_id='RedirectToOriginalLink',
    include_in_schema=False
)
async def redirect_to_original_link(
    link_id: str,
    async_session: AsyncSession = Depends(get_session),
    link_repo: LinkRepository = Depends(get_link_repo),
) -> RedirectResponse:
    fetched_link: LinkModel = await link_repo.get_by_uuid(async_session=async_session, uuid_=link_id)

    if datetime.utcnow() >= fetched_link.end_date:  # pragma: no cover
        raise LinkExpiredError

    return RedirectResponse(    # pragma: no cover
        url=fetched_link.original_link,
        status_code=status.HTTP_303_SEE_OTHER
    )
