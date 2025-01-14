import logging

from src.db.dao.rebate_claim_dao import RebateClaimDAO
from src.utils import objects_to_json

logger = logging.getLogger(__name__)


class RebateClaimService:
    def __init__(self):
        """
        Initialize the RebateClaimService with a RebateClaimDAO instance.
        """
        self.rebate_claim_dao = RebateClaimDAO()

    async def get_all_claims(self):
        """
        Fetch all rebate claims.
        """
        rebate_claims = await self.rebate_claim_dao.get_all()
        return objects_to_json(rebate_claims)

    async def get_claim_by_id(self, claim_id):
        """
        Fetch a rebate claim by its primary key (ID).
        """
        return await self.rebate_claim_dao.get_by_column_value("id", claim_id)

    async def create_claim(self, data):
        """
        Create a new rebate claim.
        :param data: A dictionary containing rebate claim data.
        """
        return await self.rebate_claim_dao.create(data)

    async def update_claim(self, claim_id, data):
        """
        Update an existing rebate claim by its ID.
        :param claim_id: The ID of the rebate claim to update.
        :param data: A dictionary containing updated rebate claim data.
        """
        return await self.rebate_claim_dao.update(claim_id, data)

    async def delete_claim(self, claim_id):
        """
        Delete a rebate claim by its ID.
        """
        return await self.rebate_claim_dao.delete(claim_id)
