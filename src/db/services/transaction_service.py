import logging

from src.db.dao.transaction_dao import TransactionDAO
from src.exceptions.db_exceptions import NotFoundException

logger = logging.getLogger(__name__)


class TransactionService:
    def __init__(self):
        """
        Initialize the TransactionService with a TransactionDAO instance.
        """
        self.transaction_dao = TransactionDAO()

    async def get_all_transactions(self):
        """
        Fetch all transactions.
        """
        return await self.transaction_dao.get_all()

    async def get_transaction_by_id(self, transaction_id, include_rebate=False):
        """
        Fetch a transaction by its primary key (ID).
        """
        # Calculating the rebate amount dynamically during retrieval.
        # Alternatively, the rebate amount could be saved during transaction
        # creation. However, this approach has a tradeoff: if the rebate
        # percentage changes later, all related transaction entries would
        # need to be updated, leading to potential inconsistencies.
        if include_rebate:
            transaction = await self.transaction_dao.get_transaction_with_rebate(
                transaction_id)
        else:
            transaction = await self.transaction_dao.get_by_column_value(
                "id", transaction_id)
        if not transaction:
            raise NotFoundException(
                f"Transaction with ID {transaction_id} not found.")
        return transaction

    async def create_transaction(self, data):
        """
        Create a new transaction.
        :param data: A dictionary containing transaction data.
        """
        return await self.transaction_dao.create(data)

    async def update_transaction(self, transaction_id, data):
        """
        Update an existing transaction by its ID.
        :param transaction_id: The ID of the transaction to update.
        :param data: A dictionary containing updated transaction data.
        """
        return await self.transaction_dao.update(transaction_id, data)

    async def delete_transaction(self, transaction_id):
        """
        Delete a transaction by its ID.
        """
        return await self.transaction_dao.delete(transaction_id)
