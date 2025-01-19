import logging

from src.controllers.controller_utils import create_response
from src.db.services.transaction_service import TransactionService
from src.utils import map_objs_to_dict, map_obj_to_dict

logger = logging.getLogger(__name__)


class TransactionController:
    def __init__(self, transaction_service: TransactionService):
        self.__transaction_service = transaction_service

    async def submit_transaction(self, payload):
        payload = payload.dict()
        response = await self.__transaction_service.create_transaction(payload)
        return create_response(map_obj_to_dict(response), 201)

    async def get_all_transactions(self):
        transactions = await self.__transaction_service.get_all_transactions()
        return create_response(map_objs_to_dict(transactions), 200)

    async def get_transaction_by_id(self, transaction_id, include_rebate):
        transaction = await self.__transaction_service.get_transaction_by_id(
            transaction_id, include_rebate)
        return create_response(map_obj_to_dict(transaction), 200)
