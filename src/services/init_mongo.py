import logging

from repositories.mongo import Mongo


logger = logging.getLogger(__name__)

app_adb = Mongo().app_adb
COLLECTION_NAMES = [
    'cliente',
    'produto',
    'carrinho_de_compras',
    'itens_do_carrinho',
    'pedido',
    'relatorio',
]


async def rm_existent_collections() -> bool:
    collection_names = await app_adb.list_collection_names()
    if len(collection_names) == 0:
        logger.info(f'Nenhuma collection existente no banco "{app_adb}"')
    else:
        for collection in collection_names:
            logger.warning(f'Deletando todos os docs na collection: "{collection}"')
            await app_adb.drop_collection(collection)
    return len(await app_adb.list_collection_names()) == 0


async def create_collections() -> bool:
    for collection in COLLECTION_NAMES:
        logger.info(f'Criando collection "{collection}"')
        await app_adb.create_collection(collection)
    return set(await app_adb.list_collection_names()) == set(COLLECTION_NAMES)
