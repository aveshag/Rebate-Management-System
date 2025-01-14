from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel

from src.controllers import transaction_controller

router = APIRouter()


class TransactionRequest(BaseModel):
    amount: float
    transaction_date: datetime
    rebate_program_id: str


@router.post('', tags=['Transaction'],
             summary="Create a new transaction"
             )
async def submit_transaction(request: TransactionRequest):
    return await transaction_controller.submit_transaction(request)
