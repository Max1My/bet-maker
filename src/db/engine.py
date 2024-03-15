from contextlib import asynccontextmanager

from sqlalchemy import NullPool, orm
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.settings import get_settings, DatabaseSettings


class Base(orm.DeclarativeBase):
    pass


class DatabaseEngine:
    def __init__(self, db_url: str, debug: bool) -> None:
        self._engine = create_async_engine(db_url, echo=debug, future=True, poolclass=NullPool)
        self._settings = get_settings(DatabaseSettings)
        self._session_factory = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._engine,
        )
        self._connection_pool = None
        self.con = None

    @asynccontextmanager
    async def session(self) -> async_sessionmaker[AsyncSession]:
        session: AsyncSession = self._session_factory()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
