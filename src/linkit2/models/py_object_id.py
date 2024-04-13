from typing import Annotated

from bson import ObjectId
from pydantic import AfterValidator, BeforeValidator


def is_valid_object_id(value: str) -> str:
    assert ObjectId.is_valid(value), f"'{value}' must be a valid ObjectId"
    return value


PyObjectId = Annotated[str, BeforeValidator(str), AfterValidator(is_valid_object_id)]
