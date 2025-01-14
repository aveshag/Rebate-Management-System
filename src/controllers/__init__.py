from src.controllers.rebate_claim_controller import RebateClaimController
from src.controllers.rebate_program_controller import \
    RebateProgramController
from src.controllers.transaction_controller import TransactionController
from src.db.services.rebate_claim_service import RebateClaimService
from src.db.services.rebate_program_service import RebateProgramService
from src.db.services.transaction_service import TransactionService

program_controller: RebateProgramController = None
claim_controller: RebateClaimController = None
transaction_controller: TransactionController = None


def register_controllers():
    global program_controller
    global claim_controller
    global transaction_controller
    rebate_program_service = RebateProgramService()
    rebate_claim_service = RebateClaimService()
    transaction_service = TransactionService()
    program_controller = RebateProgramController(rebate_program_service)
    claim_controller = RebateClaimController(rebate_claim_service)
    transaction_controller = TransactionController(transaction_service)
