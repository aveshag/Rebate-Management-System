import uuid

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
async def get_transactions():
    return await transaction_controller.get_all_transactions()


@router.get(
    '/{transaction_id}', tags=['Transaction'],
    summary="Get a transaction"
)
async def get_transaction_by_id(transaction_id: uuid.UUID,
                                include_rebate: bool = False):
    return await transaction_controller.get_transaction_by_id(transaction_id,
                                                              include_rebate)
