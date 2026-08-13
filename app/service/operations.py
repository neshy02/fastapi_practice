from fastapi import HTTPException

from app.repository import wallets as wallet_repository
from app.schemas import Operation


def add_income(operation: Operation):
    if not wallet_repository.wallet_already_exist(operation.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f'Кошелек {operation.wallet_name} не найден.'
        )

    if operation.mount <= 0:
        raise HTTPException(
            status_code=400,
            detail='Сумма дохода должна быть положительной.'
        )

    wallet = wallet_repository.add_income(operation.wallet_name, operation.mount)

    return {
        'message': 'Доход успешно добавлен.',
        'wallet_name': operation.wallet_name,
        'amount': operation.mount,
        'description': operation.description,
        'new_balance': wallet.balance

    }  

def add_expense(operation: Operation):
    if not wallet_repository.wallet_already_exist(operation.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f'Кошелек {operation.wallet_name} не найден.'
        )

    wallet = wallet_repository.get_wallet_balance_by_name(operation.wallet_name)

    if wallet.balance < operation.mount:
        raise HTTPException(
            status_code=400,
            detail=f'Недостаточно средств на кошельке. Доступно {wallet.balance}, требуется {operation.mount}.'
        )

    wallet = wallet_repository.add_expense(operation.wallet_name, operation.mount)

    return {
        'message': 'Расход успешно добавлен.',
        'wallet_name': operation.wallet_name,
        'amount': operation.mount,
        'description': operation.description,
        'new_balance': wallet.balance
    }


