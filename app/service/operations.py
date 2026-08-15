from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import SessionLocal
from app.dependency import get_db
from app.repository import wallets as wallet_repository
from app.schemas import Operation


async def add_income(db: AsyncSession, operation: Operation):
    if operation.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail='Сумма дохода должна быть положительной.'
        )


    wallet = await wallet_repository.add_income(db, operation.wallet_name, operation.amount)

    if wallet is None:
        raise HTTPException(
            status_code=404,
            detail=f'Кошелек {operation.wallet_name} не найден.'
        )
    await db.commit()
    await db.refresh(wallet)

    return {
        'message': 'Доход успешно добавлен.',
        'wallet_name': operation.wallet_name,
        'amount': operation.amount,
        'description': operation.description,
        'new_balance': wallet.balance

    }

async def add_expense(db: AsyncSession, operation: Operation):
    if operation.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail='Сумма расхода должна быть положительной.'
        )

    wallet = await wallet_repository.get_wallet_balance_by_name(db, operation.wallet_name)

    if wallet is None:
        raise HTTPException(
            status_code=404,
            detail=f'Кошелек {operation.wallet_name} не найден.'
        )

    if wallet.balance < operation.amount:
        raise HTTPException(
            status_code=400,
            detail=f'Недостаточно средств на кошельке. Доступно {wallet.balance}, требуется {operation.amount}.'
        )

    updated_wallet = await wallet_repository.add_expense(db, operation.wallet_name, operation.amount)

    await db.commit()
    await db.refresh(wallet)

    return {
        'message': 'Расход успешно добавлен.',
        'wallet_name': operation.wallet_name,
        'amount': operation.amount,
        'description': operation.description,
        'new_balance': updated_wallet.balance
        }


