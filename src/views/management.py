from fastapi import APIRouter

from abstract import SQLResult
from repositories.mongo import Mongo
from repositories.sql_db import exec_script
from app_layer.init_mongo import (
    rm_existent_collections,
    create_collections,
)


router = APIRouter(prefix='/-', tags=['management'])


@router.get('/health')
async def health_check():
    return {'status': 'healthy'}


# FIXME: response_model
@router.post('/reset_db')
async def reset_db():
    app_adb = Mongo().app_adb
    await rm_existent_collections(app_adb)
    await create_collections(app_adb)


@router.post('/seed_products', response_model=SQLResult)
async def seed_products():
    """Insere alguns produtos de exemplo para facilitar testes."""
    return exec_script('management/seed_products.sql')
