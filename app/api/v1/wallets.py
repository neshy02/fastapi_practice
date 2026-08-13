from fastapi import APIRouter

from app.schemas import CreateWallet
from app.service import wallets as wallet_service

router = APIRouter()

@router.get("/balance")
def get_balance(wallet_name: str | None = None):
    return wallet_service.get_balance(wallet_name)


@router.post('/wallet')
def create_wallet(wallet: CreateWallet):
    return wallet_service.create_wallet(wallet)


