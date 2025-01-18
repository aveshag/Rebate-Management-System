import logging

from src.db.services.rebate_claim_service import RebateClaimService
from src.utils import map_objs_to_dict, map_obj_to_dict, create_response

logger = logging.getLogger(__name__)


class RebateClaimController:
    def __init__(self, claim_service: RebateClaimService):
        self.__claim_service = claim_service

    async def create_claim(self, payload):
        payload = payload.dict()
        response = await self.__claim_service.create_claim(payload)
        return create_response(map_obj_to_dict(response), 201)

    async def get_all_claims(self):
        rebate_claims = await self.__claim_service.get_all_claims()
        return create_response(map_objs_to_dict(rebate_claims), 200)
