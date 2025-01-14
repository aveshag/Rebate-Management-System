from fastapi import APIRouter


def register_routes():
    from src.routes.rebate_program_routes import router as rebate_program_router
    from src.routes.transaction_routes import router as transaction_router
    from src.routes.rebate_claim_routes import router as rebate_claim_router

    api_routers = APIRouter()
    api_routers.include_router(rebate_program_router, prefix="/rebate_program")
    api_routers.include_router(transaction_router, prefix="/transaction")
    api_routers.include_router(rebate_claim_router, prefix="/rebate_claim")

    return api_routers
