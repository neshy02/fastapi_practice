from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

balance: dict[str, float] = {}

DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/wallet_db"

engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

