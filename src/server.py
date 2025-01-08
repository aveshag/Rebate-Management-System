import logging

from fastapi import FastAPI
from uvicorn import Config, Server
from src.constants import API_PREFIX
from src.routes import router

logger = logging.getLogger(__name__)


def __init_app():
    return FastAPI(title="Rebate Management System")


async def start_server(app):
    # TODO: use env variables
    host = "0.0.0.0"
    port = 8456

    logger.info(f"Starting server on {host}:{port}")
    server_config = Config(app=app, host=host, port=port)
    server = Server(config=server_config)
    await server.serve()


def __register_controllers(app):
    app.include_router(router=router, prefix=API_PREFIX)


async def register_server():
    app = __init_app()

    @app.get("/")
    def root():
        return 'Welcome to Rebate Management System'

    __register_controllers(app)
    await start_server(app)
