from datetime import datetime
from typing import Optional

from fastapi import APIRouter

from src.controllers import claim_controller
from src.routes.api_models import RebateClaimRequest

router = APIRouter()


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


@router.get(
    '/summary', tags=['Rebate Claim'],
    summary="Get rebate claims summary"
)
async def get_rebate_claims(start_date: Optional[datetime] = None,
                            end_date: Optional[datetime] = None):
    return await claim_controller.get_claims_summary(start_date, end_date)
