import datetime
from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, Field

from linkit2.models.py_object_id import PyObjectId


def is_non_empty_string(value: str) -> str:
    assert len(value.strip()) > 0, f"'{value}' must be a non-empty string"
    return value


NonEmptyString = Annotated[str, AfterValidator(is_non_empty_string)]


class LinkRecordAccess(BaseModel):
    last_accessed_at: datetime.datetime
    access_count: int


class LinkRecordExpiry(BaseModel):
    expires_at: datetime.datetime
    max_access_count: int


class LinkRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    original_url: NonEmptyString
    slug: NonEmptyString
    created_at: datetime.datetime
    access: LinkRecordAccess
    expiry: LinkRecordExpiry

    def __eq__(self, value: object) -> bool:
        if isinstance(value, LinkRecord):
            return self.model_dump(exclude=set(["id"])) == value.model_dump(
                exclude=set(["id"])
            )

        return super().__eq__(value)


class LinkRecordInMongoDB(LinkRecord):
    id: PyObjectId = Field(alias="_id")
