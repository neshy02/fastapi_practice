from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.v1.operations import router as operations_router
from app.api.v1.wallets import router as wallets_router
from app.database import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(wallets_router, prefix='/api/v1', tags=['Wallets'])
app.include_router(operations_router, prefix='/api/v1', tags=['Operations'])


    


