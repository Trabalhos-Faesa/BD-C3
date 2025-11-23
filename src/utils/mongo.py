import asyncio

from decouple import config
from pymongo import AsyncMongoClient, MongoClient


MONGO_CONNECTION_STRING = config('MONGO_CONNECTION_STRING')


def get_mongo_client(
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


def get_mongo_aclient(
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


mongo_client = get_mongo_client()
mongo_aclient = get_mongo_aclient()


if __name__ == '__main__':
    async def run():
        client = get_mongo_client()
        res = client.admin.command('ping')
        print(f'Ping (sync): {res}')
        client.close()

        aclient = get_mongo_aclient()
        res = await aclient.admin.command('ping')
        print(f'Ping (async): {res}')
        await aclient.close()

    asyncio.run(run())
