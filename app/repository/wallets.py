from app.database import SessionLocal
from app.models import Wallet


def wallet_already_exist(wallet_name: str) -> bool:
    db = SessionLocal()
    try:
        return db.query(Wallet).filter(Wallet.name == wallet_name).first() is not None
    finally:
        db.close()
    
def add_income(wallet_name: str, amount: float) -> float:
    db = SessionLocal()
    try:
        wallet = db.query(Wallet).filter(Wallet.name == wallet_name).first()
        wallet.amount += amount
        db.commit()
        return wallet

def get_wallet_balance_by_name(wallet_name: str) -> float:
    return balance[wallet_name]

def add_expense(wallet_name: str, amount: float) -> float:
    balance[wallet_name] -= amount
    return balance[wallet_name]

def get_all_wallets() -> dict[str, float]:
    return balance.copy()

def create_wallet(wallet_name: str, amount: float) -> float:
    balance[wallet_name] = amount
    return balance[wallet_name]
    