from app.service import operations as operation_services
from fastapi import APIRouter

from app.schemas import Operation

router = APIRouter()


@router.post("/operation/income")
async def add_income(operation: Operation):
    return await operation_services.add_income(operation)

@router.post("/operation/expense")
async def add_expense(operation: Operation):
    return await operation_services.add_expense(operation)
          
