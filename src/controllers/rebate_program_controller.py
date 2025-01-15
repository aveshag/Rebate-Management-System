import logging

from src.db.services.rebate_program_service import RebateProgramService
from src.utils import create_response, objects_to_json

logger = logging.getLogger(__name__)


class RebateProgramController:
    def __init__(self, program_service: RebateProgramService):
        self.__program_service = program_service

    async def create_program(self, payload):
        payload = payload.dict()
        await self.__program_service.create_program(payload)
        return create_response(
            {"message": "Rebate program created successfully"}, 201)

    async def get_all_programs(self):
        rebate_programs = await self.__program_service.get_all_programs()
        return create_response(objects_to_json(rebate_programs), 200)
