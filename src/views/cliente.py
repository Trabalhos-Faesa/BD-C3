# FIXME: router response_model e return types

from bson import ObjectId
from fastapi import APIRouter, HTTPException
from pymongo import ReturnDocument

from models.cliente import Cliente
from repositories.mongo import Mongo


router = APIRouter(prefix='/cliente', tags=['cliente'])

coll = Mongo().get_acoll('cliente')


@router.post('/')
async def create(cliente: Cliente) -> dict:
    res = await coll.insert_one(
        cliente.model_dump(),
    )
    return {
        'inserted_id': str(res.inserted_id),
        'acknowledged': res.acknowledged,
    }


@router.get('/')
async def read_all() -> list[Cliente]:
    res = [c async for c in coll.find({})]
    return res


@router.get('/{_id}')
async def read_one(_id: str) -> Cliente:
    res = await coll.find_one({"_id": ObjectId(_id)})
    return res


# TODO: Partial update with .patch
@router.put('/{_id}')
async def update(_id: str, cliente: Cliente) -> Cliente:
    res = await coll.find_one_and_update(
        {'_id': ObjectId(_id)},
        {
            '$set': cliente.model_dump() | {
                '_id': ObjectId(_id),
            },
        },
        return_document=ReturnDocument.AFTER,
    )
    return res


@router.delete('/{_id}')
async def delete(_id: str) -> Cliente:
    # TODO: DRY
    exists: bool = (await coll.find_one({"_id": ObjectId(_id)})) is not None
    if not exists:
        raise HTTPException(404, f"_id '{_id}' does not exists")
    res = await coll.find_one_and_delete({'_id': ObjectId(_id)})
    return res
