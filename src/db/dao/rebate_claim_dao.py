import logging

from sqlalchemy import select, insert

from src.db.dao.generic_dao import GenericDAO
from src.db.models.rebate_models import RebateClaim, RebateProgram, Transaction
from src.exceptions.db_exceptions import ValidationsExceptions, \
    NotFoundException
from src.utils import ClaimStatus

logger = logging.getLogger(__name__)


class RebateClaimDAO(GenericDAO):
    def __init__(self):
        super().__init__(RebateClaim)

    async def create(self, data):
        try:
            transaction_id = data["transaction_id"]
            claim_amount = data["claim_amount"]
            async with (self.db.get_session_context() as session):
                query = (
                    select(Transaction, RebateProgram)
                    .join(RebateProgram,
                          Transaction.rebate_program_id == RebateProgram.id)
                    .where(Transaction.id == transaction_id).with_for_update()
                )

                transaction_result = await session.execute(query)
                transaction_result = transaction_result.first()
                if not transaction_result:
                    raise NotFoundException(
                        f"Transaction with ID {transaction_id} not found.")

                transaction, rebate_program = transaction_result
                claim_query = select(RebateClaim.id).where(
                    RebateClaim.transaction_id == transaction_id)
                claim_result = await session.execute(claim_query)
                claim_result = claim_result.scalar_one_or_none()

                if claim_result:
                    raise ValidationsExceptions(
                        f"A claim with ID {claim_result} already exists for "
                        f"transaction ID {transaction_id}.")

                max_claim_amount = rebate_program.rebate_percentage * transaction.amount / 100
                if claim_amount > max_claim_amount:
                    raise ValidationsExceptions(
                        f"Claim amount exceeds the allowed limit of {max_claim_amount} "
                        f"({rebate_program.rebate_percentage}% of transaction amount).")

                claim_data = {
                    "transaction_id": transaction_id,
                    "claim_amount": claim_amount,
                    "claim_status": ClaimStatus.PENDING.value,
                }

                record_id = await session.execute(
                    insert(self.model).values(**claim_data).returning(
                        self.model.id)
                )
                await session.commit()

                new_claim = await session.get(self.model,
                                              record_id.scalar_one())
                session.expunge_all()
                return new_claim
        except Exception as e:
            logger.error(f"Error creating claim: {e}")
            raise e
