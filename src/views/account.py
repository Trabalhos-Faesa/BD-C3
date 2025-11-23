from fastapi import APIRouter, HTTPException, status

from abstract import SQLResultStatus
from models.account import LoginPayload, LoginSuccess
from repositories.sql_db import aexec_query


router = APIRouter(prefix='/account', tags=['account'])


# TODO: return a JWT and store+check the hash of the password
@router.post('/login', response_model=LoginSuccess)
async def login(credentials: LoginPayload) -> LoginSuccess:
    """
    Autentica um cliente no sistema.
    - **email**: Email do cliente
    - **senha**: Senha do cliente
    Retorna os dados do cliente se a autenticação for bem-sucedida.
    Lança HTTPException 401 se as credenciais forem inválidas.
    """
    result = await aexec_query(
        'account/login.sql',
        {'email': credentials.email}
    )

    if result['status'] == SQLResultStatus.ERROR or len(result['rows']) < 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email inválido"
        )

    cliente_data = result['rows'][0]

    # FIXME: plain-text passwords in DB!
    if cliente_data['senha'] != credentials.senha:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Senha inválida"
        )

    return LoginSuccess(
        id_cliente=cliente_data['id_cliente'],
        email=cliente_data['email'],
        nome=cliente_data['nome'],
        sobrenome=cliente_data['sobrenome']
    )
