from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, Field

from utils.pydantic import (
    PyObjectId,
    default_model_config,
)


class Produto(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias='_id')
    nome: Annotated[str, Field(min_length=1)]
    descricao: Optional[str] = None
    preco: Annotated[float, Field(ge=0)]
    quantidade_estoque: Annotated[int, Field(ge=0)] = 0
    categoria: Optional[str] = None
    data_criacao: Optional[datetime] = None

    model_config = default_model_config
