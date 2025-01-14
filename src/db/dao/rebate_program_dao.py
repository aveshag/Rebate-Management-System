import logging

from src.db.dao.generic_dao import GenericDAO
from src.db.models.rebate_models import RebateProgram

logger = logging.getLogger(__name__)


class RebateProgramDAO(GenericDAO):
    def __init__(self):
        super().__init__(RebateProgram)
