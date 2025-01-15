from fastapi import APIRouter

from src.controllers import program_controller
from src.routes.api_models import RebateProgramRequest

router = APIRouter()


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
