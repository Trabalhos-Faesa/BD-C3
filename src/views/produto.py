from fastapi import APIRouter

from abstract import SQLResult, SQLResultDict
from models.produto import Produto
from repositories.sql_db import exec_query


router = APIRouter(prefix='/produto', tags=['produto'])


@router.post('/', response_model=SQLResult[Produto])
async def create(produto: Produto) -> SQLResultDict:
    return exec_query(
        'produto/create.sql',
        produto.model_dump(),
    )


@router.get('/', response_model=SQLResult[Produto])
async def read_all() -> SQLResultDict:
    return exec_query('produto/read_all.sql')


@router.get('/{id_produto}', response_model=SQLResult[Produto])
async def read_one(id_produto: int) -> SQLResultDict:
    return exec_query(
        'produto/read_one.sql',
        {
            'id_produto': id_produto,
        },
    )


# TODO: Partial update with .patch
@router.put('/{id_produto}', response_model=SQLResult[Produto])
async def update(id_produto: int, produto: Produto) -> SQLResultDict:
    return exec_query(
        'produto/update.sql',
        produto.model_dump() | {
            'id_produto': id_produto,
        },
    )


@router.delete('/{id_produto}', response_model=SQLResult[Produto])
async def delete(id_produto: int) -> SQLResultDict:
    return exec_query(
        'produto/delete.sql',
        {
            'id_produto': id_produto,
        }
    )
