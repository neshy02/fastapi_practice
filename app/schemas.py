from decimal import Decimal

from pydantic import BaseModel, Field, field_validator


class Operation(BaseModel):
    wallet_name: str = Field(..., max_length=50)
    amount: Decimal
    description: str | None = Field(None, max_length=200)

    @field_validator('amount')
    def validate_amount(cls, value: Decimal) -> Decimal:
        if value <= 0:
            raise ValueError('Сумма должна быть положительной.')
        return value

    @field_validator('wallet_name')
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError('Имя кошелька не может быть пустым.')
        return value



class CreateWallet(BaseModel):
    name: str = Field(..., max_length=50)
    initial_balance: Decimal = 0.0
    
    @field_validator('name')
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError('Имя кошелька не может быть пустым.')
        return value

    @field_validator('initial_balance')
    def validate_initial_balance(cls, value: Decimal) -> Decimal:
        if value < 0:
            raise ValueError('Сумма должна быть положительной.')
        return value