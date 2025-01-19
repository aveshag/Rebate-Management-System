import logging

from sqlalchemy import select, insert, func, case

from src.db.dao.generic_dao import GenericDAO
from src.db.models.rebate_models import RebateClaim, RebateProgram, Transaction
from src.db.models.helper_models import ClaimsSummaryModel
from src.exceptions.db_exceptions import ValidationsExceptions, \
    NotFoundException
from src.utils import ClaimStatus

logger = logging.getLogger(__name__)


class RebateClaimDAO(GenericDAO):
    def __init__(self):
        super().__init__(RebateClaim)

    async def create(self, data):
        """
        Insert a new row into the database.
        The function ensures that only one claim exists for a transaction and
        claim amount shouldn't exceed the maximum rebate amount for the
        transaction
        """
        try:
            transaction_id = data["transaction_id"]
            claim_amount = data["claim_amount"]
            query = (
                select(Transaction, RebateProgram)
                .join(RebateProgram,
                      Transaction.rebate_program_id == RebateProgram.id)
                .where(Transaction.id == transaction_id).with_for_update()
            )
            async with (self.db.get_session_context() as session):
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

                result = await session.execute(
                    insert(self.model)
                    .values(**claim_data)
                    .returning(self.model)
                )
                new_claim = result.scalar_one()
                session.expunge_all()
                await session.commit()
                return new_claim
        except Exception as e:
            logger.error(f"Error creating claim: {e}")
            raise e

    async def get_claims_summary(self, start_date, end_date):
        """
        Prepare claim summaries for the given time period.
        """
        try:
            query = (
                select(
                    func.coalesce(func.count(), 0).label("total_claims"),
                    func.coalesce(func.sum(
                        case((RebateClaim.claim_status ==
                              ClaimStatus.PENDING.value, 1),
                             else_=0)), 0).label("pending_claims"),
                    func.coalesce(func.sum(
                        case((RebateClaim.claim_status ==
                              ClaimStatus.APPROVED.value, 1),
                             else_=0)), 0).label("approved_claims"),
                    func.coalesce(func.sum(
                        case((RebateClaim.claim_status ==
                              ClaimStatus.REJECTED.value, 1),
                             else_=0)), 0).label("rejected_claims"),
                    func.coalesce(func.sum(
                        case((RebateClaim.claim_status ==
                              ClaimStatus.APPROVED.value,
                              RebateClaim.claim_amount),
                             else_=0.0)), 0.0).label(
                        "approved_claim_amount"),
                    func.coalesce(func.sum(
                        case((
                            RebateClaim.claim_status == ClaimStatus.PENDING.value,
                            RebateClaim.claim_amount),
                            else_=0.0)), 0.0).label(
                        "pending_claim_amount"),
                )
            )
            if start_date:
                query = query.where(RebateClaim.claim_date >= start_date)
            if end_date:
                query = query.where(RebateClaim.claim_date <= end_date)
            async with self.db.get_session_context() as session:
                result = await session.execute(query)
                result = result.first()
                summary = ClaimsSummaryModel(**result._mapping)
                return summary
        except Exception as e:
            logger.error(f"Error getting claims summary: {e}")
            raise e
