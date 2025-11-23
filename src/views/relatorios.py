from fastapi import APIRouter

from abstract import SQLResult, SQLResultDict
from repositories.sql_db import aexec_query


router = APIRouter(prefix='/relatorios', tags=['relatorios'])


@router.get('/{id_cliente}', response_model=SQLResult)
async def pedidos_por_cliente(id_cliente: int) -> SQLResultDict:
    """Retorna o histórico de pedidos (com itens) para um cliente."""
    return await aexec_query(
        'relatorios/pedidos_por_cliente.sql',
        {
            'id_cliente': id_cliente,
        },
    )


@router.get('/produtos_mais_vendidos', response_model=SQLResult)
async def produtos_mais_vendidos() -> SQLResultDict:
    return await aexec_query(
        'relatorios/produtos_mais_vendidos.sql',
    )
