from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import SessionLocal
from app.models import Wallet


async def wallet_already_exist(wallet_name: str) -> bool:
    async with SessionLocal() as db:
        query = select(Wallet).filter(Wallet.name == wallet_name)
        result = await db.execute(query)
        return result.scalar_one_or_none() is not None
    
async def add_income(wallet_name: str, amount: float) -> Wallet | None:
    async with SessionLocal() as db:
        query = select(Wallet).filter(Wallet.name == wallet_name)
        result = await db.execute(query)
        wallet = result.scalar_one_or_none()

        if wallet:
            wallet.amount += amount
            await db.commit()
            await db.refresh(wallet)
        return wallet

async def get_wallet_balance_by_name(wallet_name: str) -> Wallet | None:
    async with SessionLocal() as db:
        query = select(Wallet).filter(Wallet.name == wallet_name)
        result = await db.execute(query)
        return result.scalar_one_or_none()

async def add_expense(wallet_name: str, amount: float) -> Wallet | None:
    async with SessionLocal() as db:
        query = select(Wallet).filter(Wallet.name == wallet_name)
        result = await db.execute(query)
        wallet = result.scalar_one_or_none()
        if wallet:
            wallet.amount -= amount
            await db.commit()
            await db.refresh(wallet)
        return wallet

async def get_all_wallets() -> list[Wallet]:
    async with SessionLocal() as db:
        query = select(Wallet)
        result = await db.execute(query)
        return list(result.scalars().all())


async def create_wallet(wallet_name: str, amount: float) -> Wallet:
    async with SessionLocal() as db:
        new_wallet = Wallet(name=wallet_name, balance=amount)
        db.add(new_wallet)
        await db.commit()
        await db.refresh(new_wallet)
        return new_wallet
    