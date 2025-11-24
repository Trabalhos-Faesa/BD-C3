from fastapi import APIRouter

from abstract import SQLResult
from repositories.sql_db import exec_script
from services import init_mongo


router = APIRouter(prefix='/-', tags=['management'])


@router.get('/health')
async def health_check():
    return {'status': 'healthy'}


# FIXME: response_model
@router.post('/reset_db')
async def reset_db():
    rm_existent_collections = await init_mongo.rm_existent_collections()
    create_collections = await init_mongo.create_collections()
    return {
        'rm_existent_collections': rm_existent_collections,
        'create_collections': create_collections,
    }


@router.post('/seed_products', response_model=SQLResult)
async def seed_products():
    """Insere alguns produtos de exemplo para facilitar testes."""
    return exec_script('management/seed_products.sql')
