
from fastapi import APIRouter

from abstract import SQLResult
from repositories.sql_db import exec_script


router = APIRouter(prefix='/-', tags=['management'])


@router.get('/health')
async def health_check():
    return {'status': 'healthy'}


@router.post('/reset_db', response_model=SQLResult)
async def reset_db():
    return exec_script('management/reset_db.sql')


@router.post('/seed_products', response_model=SQLResult)
async def seed_products():
    """Insere alguns produtos de exemplo para facilitar testes."""
    return exec_script('management/seed_products.sql')
