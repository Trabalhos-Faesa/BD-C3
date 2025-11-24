from bson import ObjectId
from fastapi import HTTPException
from pymongo import ReturnDocument

from models.produto import Produto
from repositories.mongo import Mongo


class ProdutoService:
    def __init__(self) -> None:
        self.collection_name = 'produto'
        self.acoll = Mongo().get_acoll(self.collection_name)

    async def create(self, produto: Produto) -> dict:
        res = await self.acoll.insert_one(
            produto.model_dump(),
        )
        return {
            'inserted_id': str(res.inserted_id),
            'acknowledged': res.acknowledged,
        }

    async def read_all(self) -> list[Produto]:
        return [c async for c in self.acoll.find({})]

    async def read_one(self, _id: str) -> Produto | None:
        res = await self.acoll.find_one({"_id": ObjectId(_id)})
        return res

    async def update(self, _id: str, produto: Produto) -> Produto:
        if (await self.read_one(_id)) is None:
            raise HTTPException(404, f"_id '{_id}' does not exists")

        return await self.acoll.find_one_and_update(
            {'_id': ObjectId(_id)},
            {
                '$set': produto.model_dump() | {
                    '_id': ObjectId(_id),
                },
            },
            return_document=ReturnDocument.AFTER,
        )

    async def delete(self, _id: str) -> Produto:
        if (await self.read_one(_id)) is None:
            raise HTTPException(404, f"_id '{_id}' does not exists")

        return await self.acoll.find_one_and_delete({'_id': ObjectId(_id)})
