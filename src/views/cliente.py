# TODO: response_model

from fastapi import APIRouter

from app_layer.cliente import ClienteService
from models.cliente import Cliente


router = APIRouter(prefix='/cliente', tags=['cliente'])
service = ClienteService()


@router.post('/')
async def create(cliente: Cliente):
    return await service.create(cliente)


@router.get('/')
async def read_all():
    return await service.read_all()


@router.get('/{_id}')
async def read_one(_id: str):
    return await service.read_one(_id)

@router.put('/{_id}')
async def update(_id: str, cliente: Cliente):
    return await service.update(_id, cliente)

# TODO: Partial update with .patch

@router.delete('/{_id}')
async def delete(_id: str):
    return await service.delete(_id)
