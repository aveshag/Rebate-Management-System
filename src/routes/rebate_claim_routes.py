from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel

from src.controllers import claim_controller

router = APIRouter()


class RebateClaimRequest(BaseModel):
    transaction_id: str
    claim_amount: int
    last_update_time: datetime


@router.post(
    '', tags=['Rebate Claim'],
    summary="Create a new rebate claim"
)
async def claim_rebate(request: RebateClaimRequest):
    return await claim_controller.create_claim(request)


@router.get(
    '', tags=['Rebate Claim'],
    summary="Get all rebate claims"
)
async def get_rebate_claims():
    return await claim_controller.get_all_claims()
