from fastapi import APIRouter

from app_layer.produto import ProdutoService
from models.produto import Produto


router = APIRouter(prefix='/produto', tags=['produto'])
service = ProdutoService()


@router.post('/')
async def create(produto: Produto) -> dict:
    return await service.create(produto)


@router.get('/')
async def read_all() -> list[Produto]:
    return await service.read_all()


@router.get('/{_id}')
async def read_one(_id: str) -> Produto | None:
    return await service.read_one(_id)


@router.put('/{_id}')
async def update(_id: str, produto: Produto) -> Produto:
    return await service.update(_id, produto)


# TODO: Partial update with .patch


@router.delete('/{_id}')
async def delete(_id: str) -> Produto:
    return await service.delete(_id)
