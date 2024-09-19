from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config import settings

async_engine = create_async_engine(
    str(settings.SQLALCHEMY_DATABASE_URI), pool_pre_ping=True
)

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine)
