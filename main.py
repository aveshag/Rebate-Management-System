import asyncio

from src.server import register_server
from src.constants import LOGGER_CONFIG
from logging import config, getLogger

from json import load

logger = getLogger(__name__)


def __init_logger():
    with open(LOGGER_CONFIG, "r") as f:
        config_dict = load(f)
        config.dictConfig(config_dict)


async def main():
    __init_logger()
    logger.info("Registering server...")
    await register_server()


if __name__ == "__main__":
    asyncio.run(main())
