from app.service import operations as operation_services
from fastapi import APIRouter

from app.schemas import Operation

router = APIRouter()


@router.post("/operation/income")
def add_income(operation: Operation):
    return operation_services.add_income(operation)

@router.post("/operation/expense")
def add_expense(operation: Operation):
    return operation_services.add_expense(operation)  
          
