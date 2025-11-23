import logging
from pymongo.asynchronous.database import AsyncDatabase


logger = logging.getLogger(__name__)

COLLECTION_NAMES = [
    'cliente',
    'produto',
    'carrinho_de_compras',
    'itens_do_carrinho',
    'pedido',
    'relatorio',
]


async def rm_existent_collections(app_adb: AsyncDatabase) -> None:
    collection_names = await app_adb.list_collection_names()
    if len(collection_names) == 0:
        logger.info(f'Nenhuma collection existente no banco "{app_adb}"')
    else:
        for collection in collection_names:
            logger.warning(f'Deletando todos os docs na collection: "{collection}"')
            app_adb[collection].delete_many({})


async def create_collections(app_adb: AsyncDatabase) -> None:
    for collection in COLLECTION_NAMES:
        logger.info(f'Criando collection "{collection}"')
        app_adb[collection]
