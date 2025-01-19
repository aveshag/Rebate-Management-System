import asyncio
import logging
import subprocess

import asyncpg

from src.constants import ALEMBIC_CONFIG
from src.utils import get_db_env_vars

logger = logging.getLogger(__name__)


async def create_db():
    username, password, host, port, db_name_to_create = get_db_env_vars()
    postgres_connection = None
    try:
        postgres_connection = await asyncpg.connect(
            user=username,
            password=password,
            host=host,
            port=port,
            database="postgres"
        )

        query = "SELECT 1 FROM pg_database WHERE datname = $1;"
        result = await postgres_connection.fetchval(query, db_name_to_create)
        if result:
            logger.info(f"Database '{db_name_to_create}' already exists.")
            return

        logger.info(f"Creating database '{db_name_to_create}'...")
        await postgres_connection.execute(
            f'CREATE DATABASE "{db_name_to_create}"')
        logger.info(f"Database '{db_name_to_create}' created successfully.")
    except Exception as ex:
        raise Exception(
            f"Error connecting to PostgreSQL or creating database: {ex}")
    finally:
        if postgres_connection:
            await postgres_connection.close()


async def run_migrations():
    logger.info("Running Alembic migrations...")
    try:
        process = await asyncio.create_subprocess_exec(
            "alembic", "-c", ALEMBIC_CONFIG, "upgrade", "head",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            logger.info("Alembic migrations applied successfully.")
        else:
            raise Exception(f"Alembic migrations failed:\n{stderr.decode()}")

    except Exception as ex:
        raise Exception(f"Error running Alembic migrations: {ex}")


async def create_db_and_run_alembic():
    await create_db()
    await run_migrations()
