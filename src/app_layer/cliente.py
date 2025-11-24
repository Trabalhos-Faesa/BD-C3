# TODO: better return types

from bson import ObjectId
from fastapi import HTTPException
from pymongo import ReturnDocument

from models.cliente import Cliente
from repositories.mongo import Mongo


class ClienteService:
    def __init__(self) -> None:
        self.collection_name = 'cliente'
        self.acoll = Mongo().get_acoll(self.collection_name)

    async def create(self, cliente: Cliente) -> dict:
        res = await self.acoll.insert_one(
            cliente.model_dump(),
        )
        return {
            'inserted_id': str(res.inserted_id),
            'acknowledged': res.acknowledged,
        }

    async def read_all(self) -> list[Cliente]:
        return [c async for c in self.acoll.find({})]

    async def read_one(self, _id: str) -> Cliente | None:
        return await self.acoll.find_one({"_id": ObjectId(_id)})

    async def update(self, _id: str, cliente: Cliente) -> Cliente:
        if (await self.read_one(_id)) is None:
            raise HTTPException(404, f"_id '{_id}' does not exists")

        return await self.acoll.find_one_and_update(
            {'_id': ObjectId(_id)},
            {
                '$set': cliente.model_dump() | {
                    '_id': ObjectId(_id),
                },
            },
            return_document=ReturnDocument.AFTER,
        )

    async def delete(self, _id: str) -> Cliente:
        if (await self.read_one(_id)) is None:
            raise HTTPException(404, f"_id '{_id}' does not exists")

        return await self.acoll.find_one_and_delete({'_id': ObjectId(_id)})
