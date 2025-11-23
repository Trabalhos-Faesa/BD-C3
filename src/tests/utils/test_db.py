import pytest
from sqlalchemy import (
    Engine,
    text,
)
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
)

from repositories.db import DBEngines


@pytest.fixture
def db_engines() -> DBEngines:
    return DBEngines()


class TestDBEngines:
    def test_singleton(self, db_engines) -> None:
        assert db_engines is DBEngines()

    def test_sync_engine_conn_data(self, db_engines) -> None:
        sync_engine: Engine = db_engines.engine
        with sync_engine.connect() as conn:
            query = 'SELECT 1;'
            assert len(conn.execute(text(query)).fetchall()) > 0, \
                'Nenhum dado obtido'

    def test_sync_engine_conn_data_fail(self, db_engines) -> None:
        sync_engine: Engine = db_engines.engine
        with sync_engine.connect() as conn:
            query = 'SELECT 1 WHERE 1=0;'
            assert len(conn.execute(text(query)).fetchall()) == 0, \
                'Dado inesperado obtido'

    @pytest.mark.asyncio
    async def test_async_engine_conn_data(self, db_engines) -> None:
        async_engine: AsyncEngine = db_engines.aengine
        async with async_engine.connect() as conn:
            query = 'SELECT 1;'
            assert len((await conn.execute(text(query))).fetchall()) > 0, \
                'Nenhum dado obtido'

    @pytest.mark.asyncio
    async def test_async_engine_conn_data_fail(self, db_engines) -> None:
        async_engine: AsyncEngine = db_engines.aengine
        async with async_engine.connect() as conn:
            query = 'SELECT 1 WHERE 1=0;'
            assert len((await conn.execute(text(query))).fetchall()) == 0, \
                'Dado inesperado obtido'
