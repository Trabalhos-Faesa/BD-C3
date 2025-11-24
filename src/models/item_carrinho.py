from typing import Annotated, Optional

from pydantic import (
    AfterValidator,
    BaseModel,
    Field,
)

from utils.pydantic import (
    PyObjectId,
    default_model_config,
)


# TODO
class CarrinhoCompra(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias='_id')
    id_cliente: int
    id_produto: int
    data_criacao: Optional[str] = None
    quantidade: Annotated[int, AfterValidator(lambda v: v if v > 0 else 1)]

    model_config = default_model_config
