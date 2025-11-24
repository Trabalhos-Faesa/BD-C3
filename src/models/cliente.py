from typing import Annotated, Optional

from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    EmailStr,
    Field,
    PlainSerializer,
    StringConstraints,
    WithJsonSchema,
)

from utils.validators import (
    valid_cpf,
    valid_senha,
    validate_object_id_str,
)


PyObjectId = Annotated[
    str,
    BeforeValidator(validate_object_id_str),
    PlainSerializer(str, return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization'),
]


class Cliente(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias='_id')
    email: EmailStr
    senha: Annotated[str, AfterValidator(valid_senha)]
    nome: str
    sobrenome: str
    cpf: Annotated[str, StringConstraints(min_length=11, max_length=11), AfterValidator(valid_cpf)]
    # -- Endereço: --
    cep: Optional[Annotated[str, StringConstraints(min_length=8, max_length=8)]] = None
    # Unidade Federativa (Estado)
    uf: Optional[Annotated[str, StringConstraints(min_length=2, max_length=2)]] = None
    cidade: Optional[str] = None
    bairro: Optional[str] = None
    rua: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None

    model_config = ConfigDict(
        {
            'populate_by_name': True,
            'arbitrary_types_allowed': True,
            # 'json_encoders': {
            #     ObjectId: str,
            # }
        }
    )
