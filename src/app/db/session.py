from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.core.config import CONFIG

async_engine = create_async_engine(
    url=CONFIG.db.url_sqlalchemy,
    pool_size=100,
    max_overflow=20,
    echo=True)

async_session = AsyncSession(bind=async_engine)
