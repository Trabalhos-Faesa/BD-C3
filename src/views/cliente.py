from fastapi import APIRouter

from abstract import SQLResult, SQLResultDict
from models.cliente import Cliente
from repositories.sql_db import aexec_query
from repositories.mongo import Mongo


router = APIRouter(prefix='/cliente', tags=['cliente'])

COLLECTION_NAME = 'cliente'


# FIXME: response_model
@router.post('/')
async def create(cliente: Cliente):
    app_adb = Mongo().app_adb
    collection = app_adb[COLLECTION_NAME]
    res = collection.insert_one(
        cliente.model_dump(),
    )
    return res


@router.get('/', response_model=SQLResult[Cliente])
async def read_all() -> SQLResultDict:
    return await aexec_query('cliente/read_all.sql')


@router.get('/{id_cliente}', response_model=SQLResult[Cliente])
async def read_one(id_cliente: int) -> SQLResultDict:
    return await aexec_query(
        'cliente/read_one.sql',
        {
            'id_cliente': id_cliente,
        },
    )


# TODO: Partial update with .patch
@router.put('/{id_cliente}', response_model=SQLResult[Cliente])
async def update(id_cliente: int, cliente: Cliente) -> SQLResultDict:
    return await aexec_query(
        'cliente/update.sql',
        cliente.model_dump() | {
            'id_cliente': id_cliente,
        },
    )


@router.delete('/{id_cliente}', response_model=SQLResult[Cliente])
async def delete(id_cliente: int) -> SQLResultDict:
    return await aexec_query(
        'cliente/delete.sql',
        {
            'id_cliente': id_cliente,
        }
    )
