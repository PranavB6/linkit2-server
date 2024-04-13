from datetime import datetime
from typing import Any

from bson import ObjectId

from linkit2.models.link_statistics_record import (
    LinkStatisticsRecord,
    LinkStatisticsRecordAccess,
    LinkStatisticsRecordExpiry,
    LinkStatisticsRecordInMongoDB,
)


class TestLinkStatisticsRecord:
    def test_create_link_statistics_record(self):
        link_statistics_record_id = ObjectId()
        link_record_id = ObjectId()
        created_at = datetime.now()
        last_accessed_at = datetime.now()
        access_count = 0
        expires_at = datetime.now()
        max_access_count = 0

        link_statistics_record = LinkStatisticsRecord(
            _id=link_statistics_record_id,  # type: ignore
            link_record_id=link_record_id,  # type: ignore
            created_at=created_at,
            access=LinkStatisticsRecordAccess(
                last_accessed_at=last_accessed_at,
                access_count=access_count,
            ),
            expiry=LinkStatisticsRecordExpiry(
                expires_at=expires_at, max_access_count=max_access_count
            ),
        )

        assert link_statistics_record is not None
        assert link_statistics_record.link_record_id == str(link_record_id)
        assert link_statistics_record.created_at == created_at
        assert link_statistics_record.access.last_accessed_at == last_accessed_at
        assert link_statistics_record.access.access_count == access_count
        assert link_statistics_record.expiry.expires_at == expires_at
        assert link_statistics_record.expiry.max_access_count == max_access_count

    def test_create_link_statistics_record_using_dict(self):
        link_statistics_record_dict: dict[str, Any] = {
            "link_record_id": ObjectId(),
            "created_at": datetime.now(),
            "access": {
                "last_accessed_at": datetime.now(),
                "access_count": 0,
            },
            "expiry": {
                "expires_at": datetime.now(),
                "max_access_count": 0,
            },
        }

        link_statistics_record = LinkStatisticsRecord(**link_statistics_record_dict)

        assert link_statistics_record is not None

        expected = link_statistics_record_dict.copy()
        expected["link_record_id"] = str(expected["link_record_id"])

        assert link_statistics_record.model_dump() == expected


class TestLinkStatisticsRecordInMongoDB:
    def test_create_link_statistics_record(self):
        link_statistics_record_id = ObjectId()
        link_record_id = ObjectId()
        created_at = datetime.now()
        last_accessed_at = datetime.now()
        access_count = 0
        expires_at = datetime.now()
        max_access_count = 0

        link_statistics_record = LinkStatisticsRecordInMongoDB(
            _id=link_statistics_record_id,  # type: ignore
            link_record_id=link_record_id,  # type: ignore
            created_at=created_at,
            access=LinkStatisticsRecordAccess(
                last_accessed_at=last_accessed_at,
                access_count=access_count,
            ),
            expiry=LinkStatisticsRecordExpiry(
                expires_at=expires_at, max_access_count=max_access_count
            ),
        )

        assert link_statistics_record is not None
        assert link_statistics_record.id == str(link_statistics_record_id)
        assert link_statistics_record.link_record_id == str(link_record_id)
        assert link_statistics_record.created_at == created_at
        assert link_statistics_record.access.last_accessed_at == last_accessed_at
        assert link_statistics_record.access.access_count == access_count
        assert link_statistics_record.expiry.expires_at == expires_at
        assert link_statistics_record.expiry.max_access_count == max_access_count

    def test_create_link_statistics_record_using_dict(self):
        link_statistics_record_dict: dict[str, Any] = {
            "_id": ObjectId(),
            "link_record_id": ObjectId(),
            "created_at": datetime.now(),
            "access": {
                "last_accessed_at": datetime.now(),
                "access_count": 0,
            },
            "expiry": {
                "expires_at": datetime.now(),
                "max_access_count": 0,
            },
        }

        link_statistics_record = LinkStatisticsRecordInMongoDB(
            **link_statistics_record_dict
        )

        assert link_statistics_record is not None

        expected = link_statistics_record_dict.copy()
        expected["id"] = str(expected.pop("_id"))
        expected["link_record_id"] = str(expected["link_record_id"])

        assert link_statistics_record.model_dump() == expected
