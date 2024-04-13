from typing import Annotated

from pydantic import AfterValidator, BaseModel, Field

from linkit2.models.py_object_id import PyObjectId


def is_non_empty_string(value: str) -> str:
    assert len(value.strip()) > 0, f"'{value}' must be a non-empty string"
    return value


NonEmptyString = Annotated[str, AfterValidator(is_non_empty_string)]


class LinkRecord(BaseModel):
    original_url: NonEmptyString


class LinkRecordInMongoDB(LinkRecord):
    id: PyObjectId = Field(alias="_id")
