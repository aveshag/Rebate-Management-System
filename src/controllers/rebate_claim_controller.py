from src.db.services.rebate_claim_service import RebateClaimService
from src.utils import create_response


class RebateClaimController:
    def __init__(self, claim_service: RebateClaimService):
        self.__claim_service = claim_service

    async def create_claim(self, data):
        await self.__claim_service.create_claim(data)
        return create_response(
            {"message": "Rebate claim created successfully"}, 201)
