import logging

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.v1.api import api_router
from app.core.config import CONFIG
from app.exceptions.api import APIError, api_error_handler
from app.core.middlewares import log_requests, add_process_time_header, validation_exception_handler
from app.api.v1.endpoints.healthz import router as health_router
from app.api.v1.endpoints.redirect import router as redirect_router

logger = logging.getLogger(__name__)

main_app = FastAPI(
    title=CONFIG.api.title,
    debug=CONFIG.api.debug,
    version=CONFIG.api.version,
    openapi_url="/openapi.json",
)

main_app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=CONFIG.api.allowed_hosts or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
main_app.add_middleware(GZipMiddleware, minimum_size=1000)
main_app.add_middleware(BaseHTTPMiddleware, dispatch=add_process_time_header)
main_app.add_middleware(BaseHTTPMiddleware, dispatch=log_requests)

main_app.add_exception_handler(RequestValidationError, validation_exception_handler)
main_app.add_exception_handler(APIError, api_error_handler)

main_app.include_router(router=api_router, prefix=CONFIG.api.prefix)
main_app.include_router(router=health_router, prefix="/healthz", tags=['API Health'])
main_app.include_router(router=redirect_router, prefix="", tags=['short link'])


if __name__ == "__main__":
    uvicorn.run("main:main_app", host="0.0.0.0", port=8000, workers=7)  # pragma: no cover
