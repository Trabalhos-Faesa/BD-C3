from fastapi import APIRouter

from abstract import SQLResult, SQLResultDict
from models.cliente import Cliente
from repositories.db import aexec_query


router = APIRouter(prefix='/cliente', tags=['cliente'])


@router.post('/', response_model=SQLResult[Cliente])
async def create(cliente: Cliente) -> SQLResultDict:
    return await aexec_query(
        'cliente/create.sql',
        cliente.model_dump(),
    )


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
