from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import SessionLocal
from app.repository import wallets as wallets_repository
from app.schemas import CreateWallet


async def get_balance(db: AsyncSession, wallet_name: str | None = None):
    if wallet_name is None:
        wallets = await wallets_repository.get_all_wallets(db)
        return {'total_balance': sum([w.balance for w in wallets])}

    wallet = await wallets_repository.get_wallet_balance_by_name(db, wallet_name)

    if wallet is None:
        raise HTTPException(
            status_code=404,
            detail=f'Кошелек {wallet_name} не найден.'
        )

    return {'wallet': wallet_name, 'balance': wallet.balance}

async def create_wallet(db: AsyncSession, wallet: CreateWallet):
    if await wallets_repository.wallet_already_exist(db, wallet.name):
         raise HTTPException(
                status_code=400,
                detail=f"Кошелек '{wallet.name}' уже существует."
            )

    new_balance = await wallets_repository.create_wallet(db, wallet.name, wallet.initial_balance)
    await db.commit()
    await db.refresh(new_balance)
 
    return {
        'message': f"Кошелек '{new_balance.name}' создан с балансом - {new_balance.balance}."
    }