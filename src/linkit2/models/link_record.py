from typing import Optional

from pydantic import BaseModel, Field

from linkit2.models.py_object_id import PyObjectId


class LinkRecord(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    original_url: str = Field(default=None)


class LinkRecordInMongoDB(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    original_url: str = Field(default=None)
