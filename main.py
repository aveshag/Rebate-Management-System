import asyncio
from logging import config, getLogger

from src.server import register_server
from src.utils import get_logger_config

logger = getLogger(__name__)


def __init_logger():
    config.dictConfig(get_logger_config())


async def main():
    __init_logger()
    logger.info("Registering server...")
    await register_server()


if __name__ == "__main__":
    asyncio.run(main())
