from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.config import settings






engine = create_async_engine(settings.DATABASE_URL)

async_session_maker = async_sessionmaker(engine,class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass