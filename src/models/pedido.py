from typing import Optional

from pydantic import BaseModel, Field

from utils.pydantic import (
    PyObjectId,
    default_model_config,
)


class Pedido(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias='_id')
    id_cliente: int
    data_pedido: Optional[str] = None
    status: str
    id_carrinho: int
    valorTotal: float

    model_config = default_model_config
