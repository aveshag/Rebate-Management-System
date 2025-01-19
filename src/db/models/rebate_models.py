import uuid

from sqlalchemy import Column, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

from src.db.models.utils import get_current_time

Base = declarative_base()
metadata = Base.metadata


class RebateProgram(Base):
    __tablename__ = 'rebate_programs'
    id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    program_name = Column(String, unique=True, nullable=False)
    rebate_percentage = Column(Float, nullable=False)
    start_date = Column(DateTime(False), nullable=False)
    end_date = Column(DateTime(False), nullable=False)
    eligibility_criteria = Column(Text, nullable=True)
    last_update_time = Column(DateTime(False), default=get_current_time,
                              nullable=False)


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    amount = Column(Float, nullable=False)
    transaction_date = Column(DateTime(False), nullable=False)
    rebate_program_id = Column(
        ForeignKey('rebate_programs.id', ondelete='RESTRICT'),
        nullable=False)
    last_update_time = Column(DateTime(False), default=get_current_time,
                              nullable=False)


class RebateClaim(Base):
    __tablename__ = 'rebate_claims'
    id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    transaction_id = Column(
        ForeignKey('transactions.id', ondelete='RESTRICT'),
        nullable=False)
    claim_amount = Column(Float, nullable=False)
    claim_status = Column(String, default='pending')
    claim_date = Column(DateTime(False), default=get_current_time,
                        nullable=False)
    last_update_time = Column(DateTime(False), default=get_current_time,
                              nullable=False)
