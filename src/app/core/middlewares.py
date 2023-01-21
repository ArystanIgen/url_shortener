# Standard Library
import time
import random
import string
import logging

from starlette import status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse


async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(dict(detail=exc.errors(), body=exc.body))
    )


async def add_process_time_header(request: Request, call_next):  # type: ignore
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


async def log_requests(request: Request, call_next):  # type: ignore
    if request.url.path == '/healthz':
        response = await call_next(request)
        return response

    logger = logging.getLogger(__name__)
    rid = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
    x_headers = dict(filter(lambda h: h[0].lower().startswith('x-'), request.headers.items()))
    logger.info(f"rid={rid} {request.method} {request.url.path} X-Headers: {x_headers}")
    start_time = time.time()

    try:
        response = await call_next(request)
    except Exception as e:
        logger.error(e)
        response = JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    formatted_process_time = '{0:.2f}'.format((time.time() - start_time) * 1000)
    logger.info(f"rid={rid} completed in={formatted_process_time}ms status code={response.status_code}")

    return response
