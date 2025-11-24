from enum import Enum
from typing import (
    Any,
    Generic,
    Mapping,
    Optional,
    TypedDict,
    TypeVar,
)

from pydantic import BaseModel


T = TypeVar("T")


class SQLResultStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"


class SQLResultDictBase(TypedDict):
    """Campos obrigatórios"""
    rows: list[Mapping[str, Any]]
    # https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.rowcount
    rowcount: int


class SQLResultDict(SQLResultDictBase, total=False):
    """Campos opcionais (`total=False`)"""
    status: Optional[SQLResultStatus]
    msg: Optional[str]


# TODO: use SQLResult[T](BaseModel) syntax and rm TypeVar declaration
class SQLResult(BaseModel, Generic[T]):
    # __annotations__ = typing.get_type_hints(SQLResultDict)
    rowcount: int
    rows: list[T]
    status: Optional[SQLResultStatus] = None
    msg: Optional[str] = None
