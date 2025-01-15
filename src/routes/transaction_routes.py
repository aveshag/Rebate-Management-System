from fastapi import APIRouter

from src.controllers import transaction_controller
from src.routes.api_models import TransactionRequest

router = APIRouter()


@router.post(
    '', tags=['Transaction'],
    summary="Create a new transaction"
)
async def submit_transaction(request: TransactionRequest):
    return await transaction_controller.submit_transaction(request)


@router.get(
    '', tags=['Transaction'],
    summary="Get all transactions"
)
async def get_rebate_claims():
    return await transaction_controller.get_all_transactions()
