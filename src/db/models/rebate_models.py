from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class RebateProgram(Base):
    __tablename__ = 'rebate_programs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    program_name = Column(String, unique=True, nullable=False)
    rebate_percentage = Column(Float, nullable=False)
    start_date = Column(DateTime(False), nullable=False)
    end_date = Column(DateTime(False), nullable=False)
    eligibility_criteria = Column(Text, nullable=True)
    last_update_time = Column(DateTime(False), nullable=False)


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Float, nullable=False)
    transaction_date = Column(DateTime(False), nullable=False)
    rebate_program_id = Column(Integer, ForeignKey('rebate_programs.id'), nullable=False)
    last_update_time = Column(DateTime(False), nullable=False)


class RebateClaim(Base):
    __tablename__ = 'rebate_claims'
    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(Integer, ForeignKey('transactions.transaction_id'), nullable=False)
    claim_amount = Column(Float, nullable=False)
    claim_status = Column(String, default='pending')
    claim_date = Column(DateTime(False), nullable=False)
    last_update_time = Column(DateTime(False), nullable=False)
