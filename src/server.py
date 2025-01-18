import logging

from fastapi import FastAPI
from uvicorn import Config, Server

from src.constants import API_PREFIX
from src.controllers import register_controllers
from src.exceptions.exception_handlers import register_exception_handlers
from src.routes import register_routes
from src.utils import get_logger_config

logger = logging.getLogger(__name__)


def __init_app():
    return FastAPI(
        title="Rebate Management System",
        version="1.0.0"
    )


async def start_server(app):
    # TODO: use env variables
    host = "0.0.0.0"
    port = 8420

    logger.info(f"Starting server on {host}:{port}")
    server_config = Config(app=app, host=host, port=port,
                           log_config=get_logger_config())
    server = Server(config=server_config)
    await server.serve()


def __register_routes(app):
    router = register_routes()
    app.include_router(router=router, prefix=API_PREFIX)


async def register_server():
    app = __init_app()

    register_exception_handlers(app)

    @app.get("/test", tags=["test"])
    def root():
        return 'Welcome to Rebate Management System'

    register_controllers()
    __register_routes(app)
    await start_server(app)
