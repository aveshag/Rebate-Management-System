from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel

from src.controllers import program_controller

router = APIRouter()


class RebateProgramRequest(BaseModel):
    program_name: str
    rebate_percentage: int
    start_date: datetime
    end_date: datetime
    eligibility_criteria: str


@router.post(
    '', tags=['Rebate Program'],
    summary="Create a new rebate program"
)
async def create_rebate_program(request: RebateProgramRequest):
    return await program_controller.create_program(request)


@router.get(
    '', tags=['Rebate Program'],
    summary="Get all rebate programs"
)
async def get_rebate_programs():
    return await program_controller.get_all_programs()
