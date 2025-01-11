import contextlib
import os
import threading

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


class Singleton(type):
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
    username = os.environ.get('DB_USERNAME')
    password = os.environ.get('DB_PASSWORD')
    host = os.environ.get('DB_HOST')
    port = os.environ.get('DB_PORT')
    db_name = os.environ.get('DB_NAME')
    return f"postgresql+asyncpg://{username}:{password}@{host}:{port}/{db_name}"


class DBSessionManager(metaclass=Singleton):
    _engine = None
    _session_factory = None

    def __init__(self):
        self.session = None
        self.db_url = build_db_url()

        self.pool_size = int(os.environ.get('DB_POOL_SIZE', 5))
        self.max_overflow = int(os.environ.get('DB_MAX_OVERFLOW', 20))
        self.pool_recycle_timeout = int(os.environ.get(
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
        session = self._session_factory()
        try:
            yield session
            if auto_commit:
                await session.commit()
                await session.flush()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
