import logging

from src.db.services.rebate_program_service import RebateProgramService
from src.utils import create_response, get_current_time

logger = logging.getLogger(__name__)


class RebateProgramController:
    def __init__(self, program_service: RebateProgramService):
        self.__program_service = program_service

    async def create_program(self, data):
        data = data.dict()
        await self.__program_service.create_program(data)
        return create_response(
            {"message": "Rebate program created successfully"}, 201)

    async def get_all_programs(self):
        return create_response(await self.__program_service.get_all_programs(),
                               200)
