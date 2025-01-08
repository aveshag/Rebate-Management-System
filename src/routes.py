from fastapi import APIRouter

router = APIRouter()


@router.get("/rebate-programs")
async def get_rebate_programs():
    return []
