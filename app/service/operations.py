from fastapi import HTTPException

from app.repository import wallets as wallet_repository
from app.schemas import Operation


async def add_income(operation: Operation):
    if operation.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail='Сумма дохода должна быть положительной.'
        )

    wallet = await wallet_repository.add_income(operation.wallet_name, operation.amount)
    if wallet is None:
        raise HTTPException(
            status_code=404,
            detail=f'Кошелек {operation.wallet_name} не найден.'
        )

    return {
        'message': 'Доход успешно добавлен.',
        'wallet_name': operation.wallet_name,
        'amount': operation.amount,
        'description': operation.description,
        'new_balance': wallet.balance

    }  

async def add_expense(operation: Operation):
    if not await wallet_repository.wallet_already_exist(operation.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f'Кошелек {operation.wallet_name} не найден.'
        )

    wallet = await wallet_repository.get_wallet_balance_by_name(operation.wallet_name)

    if wallet.balance < operation.amount:
        raise HTTPException(
            status_code=400,
            detail=f'Недостаточно средств на кошельке. Доступно {wallet.balance}, требуется {operation.amount}.'
        )

    wallet = await wallet_repository.add_expense(operation.wallet_name, operation.amount)

    return {
        'message': 'Расход успешно добавлен.',
        'wallet_name': operation.wallet_name,
        'amount': operation.amount,
        'description': operation.description,
        'new_balance': wallet.balance
    }


