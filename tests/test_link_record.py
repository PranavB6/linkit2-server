import datetime
from typing import Any

import pytest
from pydantic import ValidationError

from linkit2.models.link_record import LinkRecord
from linkit2.utils import deep_merge

valid_link_record_dict = {
    "original_url": "https://www.google.com",
    "created_at": datetime.datetime.now(),
    "access": {
        "last_accessed_at": datetime.datetime.now(),
        "access_count": 1,
    },
    "expiry": {
        "expires_at": datetime.datetime.now(),
        "max_access_count": 1,
    },
}


class TestLinkRecord:
    def test_create_link_record(self):
        link_record = LinkRecord.model_validate(valid_link_record_dict)

        assert link_record is not None

    def test_create_link_record_with_empty_dict(self):
        with pytest.raises(ValidationError):
            LinkRecord.model_validate({})

    @pytest.mark.parametrize(
        "link_record_partial_dict",
        [
            {"original_url": None},
            {"original_url": ""},
            {"created_at": None},
            {"access": None},
            {"access": {"last_accessed_at": None}},
            {
                "access": {
                    "last_accessed_at": "invalid datetime",
                },
            },
            {"access": {"access_count": None}},
            {"access": {"access_count": "invalid int"}},
            {"expiry": None},
            {"expiry": {"expires_at": None}},
            {"expiry": {"max_access_count": None}},
            {
                "access": None,
                "expiry": None,
                "original_url": None,
                "created_at": None,
            },
        ],
    )
    def test_invalid_link_record(self, link_record_partial_dict: dict[str, Any]):
        with pytest.raises(ValidationError):
            link_record_dict = deep_merge(
                valid_link_record_dict, link_record_partial_dict
            )
            LinkRecord.model_validate(link_record_dict)
