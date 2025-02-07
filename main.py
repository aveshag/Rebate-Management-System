import asyncio
from logging import config, getLogger

from src.init_db import create_db_and_run_alembic
from src.server import register_server
from src.utils import get_logger_config

logger = getLogger(__name__)


def __init_logger():
    config.dictConfig(get_logger_config())


async def main():
    __init_logger()

    logger.info("Initializing database...")
    await create_db_and_run_alembic()

    logger.info("Registering server...")
    await register_server()


if __name__ == "__main__":
    asyncio.run(main())
