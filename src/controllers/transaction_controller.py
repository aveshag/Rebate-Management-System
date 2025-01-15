import logging

from src.db.services.transaction_service import TransactionService
from src.utils import create_response, objects_to_json

logger = logging.getLogger(__name__)


class TransactionController:
    def __init__(self, transaction_service: TransactionService):
        self.__transaction_service = transaction_service

    async def submit_transaction(self, payload):
        payload = payload.dict()
        await self.__transaction_service.create_transaction(payload)
        return create_response(
            {"message": "Transaction recorded successfully"}, 201)

    async def get_all_transactions(self):
        transactions = await self.__transaction_service.get_all_transactions()
        return create_response(objects_to_json(transactions), 200)
