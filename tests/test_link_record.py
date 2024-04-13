from typing import Any

import pytest
from bson import ObjectId
from pydantic_core import ValidationError

from linkit2.models.link_record import LinkRecord, LinkRecordInMongoDB


class TestLinkRecord:
    def test_create_link_record(self):
        original_url = "https://www.google.com"

        link_record = LinkRecord(original_url=original_url)

        assert link_record is not None
        assert link_record.original_url == original_url

    def test_create_link_record_using_dict(self):
        link_record_dict = {"original_url": "https://www.google.com"}

        link_record = LinkRecord(**link_record_dict)

        assert link_record is not None
        assert link_record.original_url == link_record_dict["original_url"]

    @pytest.mark.parametrize(
        "link_record_dict",
        [
            {},
            {"original_url": None},
            {"original_url": ""},
            {"original_url": "   "},
        ],
    )
    def test_create_link_record_using_invalid_dict(
        self, link_record_dict: dict[str, Any]
    ):
        with pytest.raises(ValidationError):
            LinkRecord(**link_record_dict)


class TestLinkRecordInMongoDB:
    def test_create_link_record_in_mongodb(self):
        object_id = ObjectId()
        original_url = "https://www.google.com"

        link_record = LinkRecordInMongoDB(
            _id=object_id,  # type: ignore
            original_url=original_url,
        )

        assert link_record is not None
        assert link_record.id == str(object_id)

    def test_create_link_record_in_mongodb_using_dict(self):
        link_record_dict = {"_id": ObjectId(), "original_url": "https://www.google.com"}

        link_record = LinkRecordInMongoDB(**link_record_dict)  # type: ignore

        assert link_record is not None

        assert link_record.id == str(link_record_dict["_id"])

    @pytest.mark.parametrize(
        "link_record_dict",
        [
            {},
            {"_id": ObjectId(), "original_url": None},
            {"_id": ObjectId(), "original_url": ""},
            {"_id": ObjectId(), "original_url": "   "},
            {"_id": None, "original_url": "https://www.google.com"},
            {"_id": "", "original_url": "https://www.google.com"},
            {"_id": "random-string", "original_url": "https://www.google.com"},
        ],
    )
    def test_create_link_record_in_mongodb_using_invalid_dict(
        self, link_record_dict: dict[str, Any]
    ):
        with pytest.raises(ValidationError):
            LinkRecordInMongoDB(**link_record_dict)
