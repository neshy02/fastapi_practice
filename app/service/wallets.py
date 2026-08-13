from fastapi import HTTPException

from app.repository import wallets as wallets_repository
from app.schemas import CreateWallet


async def get_balance(wallet_name: str | None = None):
    if wallet_name is None:
        wallets = await wallets_repository.get_all_wallets()
        return {'total_balance': sum([w.balance for w in wallets])}

    wallet = await wallets_repository.get_wallet_balance_by_name(wallet_name)

    if wallet is None:
        raise HTTPException(
            status_code=404,
            detail=f'Кошелек {wallet_name} не найден.'
        )

    return {'wallet': wallet_name, 'balance': wallet.balance}

async def create_wallet(wallet: CreateWallet):
    if await wallets_repository.wallet_already_exist(wallet.name):
        raise HTTPException(
            status_code=400,
            detail=f"Кошелек '{wallet.name}' уже существует."
        )

    new_balance = await wallets_repository.create_wallet(wallet.name, wallet.initial_balance)
 
    return {
        'message': f"Кошелек '{new_balance.name}' создан с балансом - {new_balance.balance}."
    }