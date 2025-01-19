import uuid
from datetime import datetime
from pydantic import BaseModel


class TransactionRebateModel(BaseModel):
    id: uuid.UUID
    amount: float
    transaction_date: datetime
    rebate_program_id: uuid.UUID
    last_update_time: datetime
    rebate_amount: float
