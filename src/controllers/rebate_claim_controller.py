import logging

from src.db.services.rebate_claim_service import RebateClaimService
from src.utils import create_response, objects_to_json

logger = logging.getLogger(__name__)


class RebateClaimController:
    def __init__(self, claim_service: RebateClaimService):
        self.__claim_service = claim_service

    async def create_claim(self, payload):
        payload = payload.dict()
        await self.__claim_service.create_claim(payload)
        return create_response(
            {"message": "Rebate claim created successfully"}, 201)

    async def get_all_claims(self):
        rebate_claims = await self.__claim_service.get_all_claims()
        return create_response(objects_to_json(rebate_claims), 200)
