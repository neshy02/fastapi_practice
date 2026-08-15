from sqlalchemy.ext.asyncio import AsyncSession

from app.dependency import get_db
from app.service import operations as operation_services
from fastapi import APIRouter, Depends

from app.schemas import Operation

router = APIRouter()


@router.post("/operation/income")
async def add_income(operation: Operation, db: AsyncSession = Depends(get_db)):
    return await operation_services.add_income(db, operation)

@router.post("/operation/expense")
async def add_expense(operation: Operation, db: AsyncSession = Depends(get_db)):
    return await operation_services.add_expense(db, operation)
          
