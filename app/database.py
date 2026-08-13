from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base, DeclarativeBase


DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/wallet_db"

engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass

