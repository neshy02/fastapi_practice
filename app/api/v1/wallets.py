from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependency import get_db
from app.schemas import CreateWallet
from app.service import wallets as wallet_service

router = APIRouter()

@router.get("/balance")
async def get_balance(wallet_name: str | None = None, db: AsyncSession = Depends(get_db)):
    return await wallet_service.get_balance(db, wallet_name)


@router.post('/wallet')
async def create_wallet(wallet: CreateWallet, db: AsyncSession = Depends(get_db)):
    return await wallet_service.create_wallet(db, wallet)


