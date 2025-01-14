from src.db.services.transaction_service import TransactionService
from src.utils import create_response


class TransactionController:
    def __init__(self, transaction_service: TransactionService):
        self.__transaction_service = transaction_service

    async def submit_transaction(self, data):
        await self.__transaction_service.create_transaction(data)
        return create_response(
            {"message": "Transaction recorded successfully"}, 201)
