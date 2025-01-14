import logging

from src.db.dao.generic_dao import GenericDAO
from src.db.models.rebate_models import RebateClaim

logger = logging.getLogger(__name__)


class RebateClaimDAO(GenericDAO):
    def __init__(self):
        super().__init__(RebateClaim)
