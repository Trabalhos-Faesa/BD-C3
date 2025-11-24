"""Pydantic related utilities"""

from typing import Annotated

from pydantic import (
    BeforeValidator,
    ConfigDict,
    PlainSerializer,
    WithJsonSchema,
)

from utils.validators import (
    validate_object_id_str,
)


default_model_config: ConfigDict = {
    'populate_by_name': True,
    'arbitrary_types_allowed': True,
    # 'json_encoders': {
    #     ObjectId: str,
    # }
}

PyObjectId = Annotated[
    str,
    BeforeValidator(validate_object_id_str),
    PlainSerializer(str, return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization'),
]
