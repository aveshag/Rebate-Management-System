import logging
from typing import Optional

from sqlalchemy import insert, select

from src.db.dao.generic_dao import GenericDAO
from src.db.models.helper_models import TransactionRebateModel
from src.db.models.rebate_models import RebateProgram
from src.db.models.rebate_models import Transaction
from src.exceptions.db_exceptions import ValidationsExceptions, \
    NotFoundException

logger = logging.getLogger(__name__)


class TransactionDAO(GenericDAO):
    def __init__(self):
        super().__init__(Transaction)

    async def create(self, data):
        """
        Insert a new row into the database.
        The function ensures that a transaction start date is valid
        with respect to the rebate program period and prevents concurrent
        updates to the rebate program record during validation.
        """
        try:
            async with self.db.get_session_context() as session:
                rebate_program_id = data.get("rebate_program_id")
                rebate_program_query = select(RebateProgram).where(
                    RebateProgram.id == rebate_program_id).with_for_update()

                result = await session.execute(rebate_program_query)
                rebate_program: Optional[
                    RebateProgram] = result.scalar_one_or_none()

                if not rebate_program:
                    raise NotFoundException(
                        f"Rebate program with ID {rebate_program_id} not found.")

                transaction_start_date = data.get("transaction_date")
                if rebate_program.start_date > transaction_start_date \
                        or transaction_start_date > rebate_program.end_date:
                    raise ValidationsExceptions(
                        "Transaction start date must fall within the rebate program's period.")

                result = await session.execute(
                    insert(self.model)
                    .values(**data)
                    .returning(self.model)
                )
                new_record = result.scalar_one()
                session.expunge_all()
                await session.commit()
                return new_record
        except Exception as e:
            logger.error(f"Error creating record: {e}")
            raise e

    async def get_transaction_with_rebate(self, transaction_id):
        """
            Retrieves a transaction along with its computed rebate amount.
        """
        try:
            async with self.db.get_session_context() as session:
                query = (
                    select(
                        *[getattr(Transaction, column.name) for column in
                          Transaction.__table__.columns],
                        (Transaction.amount *
                         RebateProgram.rebate_percentage / 100).label(
                            "rebate_amount")
                    )
                    .join(RebateProgram,
                          Transaction.rebate_program_id == RebateProgram.id)
                    .where(Transaction.id == transaction_id)
                )

                result = await session.execute(query)
                result = result.first()
                transaction_with_rebate = None
                if result:
                    transaction_with_rebate = TransactionRebateModel(
                        **result._mapping)
                return transaction_with_rebate
        except Exception as e:
            logger.error(f"Error fetching transaction with rebate: {e}")
            raise e
