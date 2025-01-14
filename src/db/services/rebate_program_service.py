import logging

from src.db.dao.rebate_program_dao import RebateProgramDAO
from src.utils import objects_to_json

logger = logging.getLogger(__name__)


class RebateProgramService:
    def __init__(self):
        """
        Initialize the RebateProgramService with a RebateProgramDAO instance.
        """
        self.rebate_program_dao = RebateProgramDAO()

    async def get_all_programs(self):
        """
        Fetch all rebate programs.
        """
        rebate_programs = await self.rebate_program_dao.get_all()
        return objects_to_json(rebate_programs)

    async def get_program_by_id(self, program_id):
        """
        Fetch a rebate program by its primary key (ID).
        """
        return await self.rebate_program_dao.get_by_column_value("id",
                                                                 program_id)

    async def create_program(self, data):
        """
        Create a new rebate program.
        :param data: A dictionary containing rebate program data.
        """
        return await self.rebate_program_dao.create(data)

    async def update_program(self, program_id, data):
        """
        Update an existing rebate program by its ID.
        :param program_id: The ID of the rebate program to update.
        :param data: A dictionary containing updated rebate program data.
        """
        return await self.rebate_program_dao.update(program_id, data)

    async def delete_program(self, program_id):
        """
        Delete a rebate program by its ID.
        """
        return await self.rebate_program_dao.delete(program_id)
