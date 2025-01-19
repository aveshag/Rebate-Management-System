import contextlib
import threading
from os import environ

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


class Singleton(type):
    """
    A metaclass to implement the Singleton design pattern.
    """
    _instance = None
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(Singleton, cls).__call__(*args,
                                                                   **kwargs)
        return cls._instance


def build_db_url() -> str:
    username = environ.get('DB_USERNAME', "postgres")
    password = environ.get('DB_PASSWORD', "postgres")
    host = environ.get('DB_HOST', "0.0.0.0")
    port = environ.get('DB_PORT', 5432)
    db_name = environ.get('DB_NAME', "rebate")
    return f"postgresql+asyncpg://{username}:{password}@{host}:{port}/{db_name}"


class DBSessionManager(metaclass=Singleton):
    _engine = None
    _session_factory = None

    def __init__(self):
        self.session = None
        self.db_url = build_db_url()

        self.pool_size = int(environ.get('DB_POOL_SIZE', 5))
        self.max_overflow = int(environ.get('DB_MAX_OVERFLOW', 20))
        self.pool_recycle_timeout = int(environ.get(
            'DB_POOL_RECYCLE_TIMEOUT', 30))

        if self._engine is None:
            self._engine = create_async_engine(
                self.db_url, pool_size=self.pool_size,
                max_overflow=self.max_overflow,
                pool_recycle=self.pool_recycle_timeout)

        if self._session_factory is None:
            self._session_factory = async_sessionmaker(bind=self._engine)

    def get_engine(self):
        return self._engine

    @contextlib.asynccontextmanager
    async def get_session_context(self, auto_commit: bool = True):
        """
        Provide an asynchronous context manager for database session operations.
        This context manager creates a new session, commits changes if
        `auto_commit` is enabled, and handles errors by rolling back the
        session if an exception occurs. Regardless of success or failure,
        the session is closed at the end of the context.
        """
        session = self._session_factory()
        try:
            yield session
            if auto_commit:
                await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def dispose_engine(self):
        if self._engine:
            await self._engine.dispose()
