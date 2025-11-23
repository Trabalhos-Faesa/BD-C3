import pytest

from repositories.mongo import Mongo


@pytest.fixture
def mongo() -> Mongo:
    return Mongo()


class TestMongoConn:
    def test_client_conn(self, mongo: Mongo) -> None:
        assert mongo.client.admin.command('ping') == {'ok': 1.0}

    @pytest.mark.asyncio
    async def test_aclient_conn(self, mongo: Mongo) -> None:
        assert (await mongo.aclient.admin.command('ping')) == {'ok': 1.0}
