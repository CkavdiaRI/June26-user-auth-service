from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import settings


engine = create_async_engine(settings.database_url, echo=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)
# egnine is shared database engine
# sessionlocal is the factory that creates engine
# session is one particular session

async def get_db():
    async with SessionLocal() as session:
        yield session