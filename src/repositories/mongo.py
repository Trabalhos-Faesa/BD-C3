import asyncio

from decouple import config
from pymongo import AsyncMongoClient, MongoClient
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.database import Database

from utils.abstract import Singleton


MONGO_CONNECTION_STRING = config('MONGO_CONNECTION_STRING')

APP_DB_NAME = 'app'


class Mongo(metaclass=Singleton):
    def __init__(self) -> None:
        self._client: MongoClient | None = None
        self._aclient: AsyncMongoClient | None = None
        self._app_db: Database | None = None
        self._app_adb: AsyncDatabase | None = None

    @property
    def client(self) -> MongoClient:
        if self._client is None:
            self._client: MongoClient = self.get_client()
        return self._client

    @property
    def aclient(self) -> AsyncMongoClient:
        if self._aclient is None:
            self._aclient: MongoClient = self.get_aclient()
        return self._aclient

    @property
    def app_db(self) -> Database:
        if self._app_db is None:
            self._app_db: MongoClient = self.client[APP_DB_NAME]
        return self._app_db

    @property
    def app_adb(self) -> AsyncDatabase:
        if self._app_adb is None:
            self._app_adb: MongoClient = self.aclient[APP_DB_NAME]
        return self._app_adb

    @staticmethod
    def get_client(
        connection_string: str = MONGO_CONNECTION_STRING,
        *args,
        **kwargs,
    ) -> MongoClient:
        client = MongoClient(
            connection_string,
            *args,
            **kwargs,
        )
        return client

    @staticmethod
    def get_aclient(
        connection_string: str = MONGO_CONNECTION_STRING,
        *args,
        **kwargs,
    ) -> AsyncMongoClient:
        client = AsyncMongoClient(
            connection_string,
            *args,
            **kwargs,
        )
        return client


if __name__ == '__main__':
    async def run():
        client = Mongo().client
        res = client.admin.command('ping')
        print(f'Ping (sync): {res}')
        client.close()

        aclient = Mongo().aclient
        res = await aclient.admin.command('ping')
        print(f'Ping (async): {res}')
        await aclient.close()

    asyncio.run(run())
