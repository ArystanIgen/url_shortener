from fastapi import APIRouter

# App Imports
from app.api.v1.endpoints.link import router as url_router

api_router = APIRouter()

api_router.include_router(
    prefix='/link',
    router=url_router,
    tags=['link']
)
