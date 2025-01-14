import logging

from src.db.dao.generic_dao import GenericDAO
from src.db.models.rebate_models import Transaction

logger = logging.getLogger(__name__)


class TransactionDAO(GenericDAO):
    def __init__(self):
        super().__init__(Transaction)
