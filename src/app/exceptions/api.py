# Standard Library
from typing import Dict

from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

# App Imports
from app.schemas.enums import StrEnum


class Code(StrEnum):
    LinkNotFound = "LinkNotFound"
    LinkExpiredError = "LinkExpiredError"
    InvalidIntervalError = "InvalidIntervalError"


class APIError(Exception):
    __slots__ = ('code', 'message', 'status_code')

    def __init__(self, code: Code, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code

    def to_dict(self) -> Dict[str, str]:
        return {
            'code': self.code,
            'message': self.message,
        }


async def api_error_handler(_: Request, error: APIError) -> JSONResponse:
    return JSONResponse(
        status_code=error.status_code,
        content=error.to_dict()
    )


class LinkNotFoundError(APIError):
    def __init__(self) -> None:
        super().__init__(
            code=Code.LinkNotFound,
            message='Ссылка не найдена',
            status_code=status.HTTP_404_NOT_FOUND
        )


class LinkExpiredError(APIError):
    def __init__(self) -> None:
        super().__init__(
            code=Code.LinkExpiredError,
            message='Link is expired',
            status_code=status.HTTP_403_FORBIDDEN
        )


class InvalidIntervalError(APIError):  # pragma: no cover
    def __init__(self) -> None:
        super().__init__(
            code=Code.InvalidIntervalError,
            message='Неверно задан интервал.',
            status_code=status.HTTP_400_BAD_REQUEST
        )
