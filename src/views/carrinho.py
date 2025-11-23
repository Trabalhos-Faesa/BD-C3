from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from abstract import SQLResult, SQLResultDict, SQLResultStatus
from repositories.db import exec_query


router = APIRouter(prefix='/carrinho', tags=['carrinho'])


class StartCartPayload(BaseModel):
    id_cliente: int = Field(gt=0)


@router.post('/', response_model=SQLResult[dict])
async def start_or_get_cart(payload: StartCartPayload) -> SQLResultDict:
    return exec_query(
        'carrinho/create_or_get_open.sql',
        {'id_cliente': payload.id_cliente},
    )


class AddItemPayload(BaseModel):
    id_produto: int = Field(gt=0)
    quantidade: int = Field(gt=0, description='Quantidade a adicionar (deve ser > 0)')


@router.post('/{id_carrinho}/item', response_model=SQLResult[dict])
async def add_item(id_carrinho: int, payload: AddItemPayload) -> SQLResultDict:
    result = exec_query(
        'carrinho/add_item.sql',
        {
            'id_carrinho': id_carrinho,
            'id_produto': payload.id_produto,
            'quantidade': payload.quantidade,
        },
    )

    if result['status'] == SQLResultStatus.ERROR or result['rowcount'] == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Estoque insuficiente, carrinho inexistente/fechado ou produto inválido.',
        )

    return result


@router.get('/{id_carrinho}/itens', response_model=SQLResult[dict])
async def read_items(id_carrinho: int) -> SQLResultDict:
    return exec_query(
        'carrinho/read_items.sql',
        {'id_carrinho': id_carrinho},
    )


@router.post('/{id_carrinho}/finalizar', response_model=SQLResult[dict])
async def finalizar_compra(id_carrinho: int) -> SQLResultDict:
    """Fecha o carrinho e gera um pedido com o valor total."""
    result = exec_query(
        'pedido/create_from_cart.sql',
        {'id_carrinho': id_carrinho},
    )

    if result['status'] == SQLResultStatus.ERROR or result['rowcount'] == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Carrinho vazio, já fechado ou inexistente.',
        )

    return result


class RemoveQuantityPayload(BaseModel):
    quantidade: int = Field(gt=0, description='Quantidade a remover (deve ser > 0)')


@router.post('/{id_carrinho}/item/{id_produto}/remover', response_model=SQLResult[dict])
async def remove_quantity(id_carrinho: int, id_produto: int, payload: RemoveQuantityPayload) -> SQLResultDict:
    result = exec_query(
        'carrinho/decrement_item.sql',
        {
            'id_carrinho': id_carrinho,
            'id_produto': id_produto,
            'quantidade': payload.quantidade,
        },
    )
    if result['status'] == SQLResultStatus.ERROR or result['rowcount'] == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Carrinho/item inexistente, fechado ou quantidade inválida.',
        )
    return result


@router.delete('/{id_carrinho}/item/{id_produto}', response_model=SQLResult[dict])
async def remove_item(id_carrinho: int, id_produto: int) -> SQLResultDict:
    result = exec_query(
        'carrinho/remove_item.sql',
        {
            'id_carrinho': id_carrinho,
            'id_produto': id_produto,
        },
    )
    if result['status'] == SQLResultStatus.ERROR or result['rowcount'] == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Carrinho/item inexistente ou fechado.',
        )
    return result
