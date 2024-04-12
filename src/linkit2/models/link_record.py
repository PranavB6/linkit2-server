from typing import Optional

from linkit2.models.py_object_id import PyObjectId
from pydantic import BaseModel, Field


class LinkRecord(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    original_url: str = Field(default=None)


class LinkRecordInMongoDB(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    original_url: str = Field(default=None)
