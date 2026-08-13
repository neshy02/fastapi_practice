from fastapi import APIRouter

from app.schemas import CreateWallet
from app.service import wallets as wallet_service

router = APIRouter()

@router.get("/balance")
async def get_balance(wallet_name: str | None = None):
    return await wallet_service.get_balance(wallet_name)


@router.post('/wallet')
async def create_wallet(wallet: CreateWallet):
    return await wallet_service.create_wallet(wallet)


