from typing import Annotated, Optional

from pydantic import BaseModel, BeforeValidator, Field

PyObjectId = Annotated[str, BeforeValidator(str)]


class LinkRecord(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    url: str = Field(default=None)


class LinkRecordInMongoDB(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    url: str = Field(default=None)
