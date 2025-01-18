import logging

from src.controllers.controller_utils import create_response
from src.db.services.rebate_program_service import RebateProgramService
from src.utils import map_objs_to_dict, map_obj_to_dict

logger = logging.getLogger(__name__)


class RebateProgramController:
    def __init__(self, program_service: RebateProgramService):
        self.__program_service = program_service

    async def create_program(self, payload):
        payload = payload.dict()
        response = await self.__program_service.create_program(payload)
        return create_response(map_obj_to_dict(response), 201)

    async def get_all_programs(self):
        rebate_programs = await self.__program_service.get_all_programs()
        return create_response(
            map_objs_to_dict(rebate_programs, "program_name"), 200)
