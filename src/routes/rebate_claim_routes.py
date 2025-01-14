from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel

from src.controllers import claim_controller

router = APIRouter()


class RebateClaimRequest(BaseModel):
    transaction_id: str
    claim_amount: int
    eligibility_criteria: str
    last_update_time: datetime


@router.post('', tags=['Rebate Claim'],
             summary="Create a new claim request"
             )
async def claim_rebate(request: RebateClaimRequest):
    return await claim_controller.create_claim(request)
