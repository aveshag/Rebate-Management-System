import uuid
from datetime import datetime

from pydantic import Field, field_validator, BaseModel


class RebateProgramRequest(BaseModel):
    program_name: str
    rebate_percentage: int = Field(
        ..., ge=0, le=100,
        description="Rebate percentage must be between 0 and 100.")
    start_date: datetime
    end_date: datetime
    eligibility_criteria: str

    @field_validator("end_date", mode="after")
    def validate_end_date_after_start(cls, end_date, values):
        """Ensure that end_date is after start_date."""
        # For field validators, the already validated data can be accessed
        # using the data property
        start_date = values.data.get("start_date")
        if start_date:
            if end_date <= start_date:
                raise ValueError("End date must be after start date.", )
        return end_date


class RebateClaimRequest(BaseModel):
    transaction_id: uuid.UUID
    claim_amount: float


class TransactionRequest(BaseModel):
    amount: float = Field(
        ..., ge=0, description="Transaction amount must be greater than 0.")
    transaction_date: datetime
    rebate_program_id: uuid.UUID
