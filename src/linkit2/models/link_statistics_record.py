from datetime import datetime

from pydantic import BaseModel, Field

from linkit2.models.py_object_id import PyObjectId


class LinkStatisticsRecordAccess(BaseModel):
    last_accessed_at: datetime
    access_count: int


class LinkStatisticsRecordExpiry(BaseModel):
    expires_at: datetime
    max_access_count: int


class LinkStatisticsRecord(BaseModel):
    link_record_id: PyObjectId
    created_at: datetime
    access: LinkStatisticsRecordAccess
    expiry: LinkStatisticsRecordExpiry


class LinkStatisticsRecordInMongoDB(LinkStatisticsRecord):
    id: PyObjectId = Field(alias="_id")
