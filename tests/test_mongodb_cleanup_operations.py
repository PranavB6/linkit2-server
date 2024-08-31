import datetime

import pytest

from linkit2.link_record_builder import LinkRecordBuilder
from linkit2.linkit_settings import get_linkit_settings
from linkit2.mongodb import MongoDB


@pytest.mark.mongodb
class TestMongoDBCleanup:
    def setup_class(self):
        settings = get_linkit_settings()
        self.mongodb = MongoDB(settings.mongodb)

    def setup_method(self):
        self.mongodb.delete_database()

    def test_find_expired_link_records_with_no_records(self):
        expired_link_records = self.mongodb.find_expired_link_records()

        assert len(expired_link_records) == 0

    def test_find_expired_link_records_with_expired_records(self):
        past_datetime = (
            datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(days=1)
        ).replace(microsecond=0)

        link_record = (
            LinkRecordBuilder()
            .with_expiry(
                expires_at=past_datetime,
            )
            .build()
        )

        self.mongodb.insert_link_record(link_record)

        expired_link_records = self.mongodb.find_expired_link_records()

        assert len(expired_link_records) == 1
        assert link_record == expired_link_records[0]

    def test_find_expired_link_records_with_hits_above_threshold(self):
        link_record = (
            LinkRecordBuilder()
            .with_access(
                access_count=11,
            )
            .with_expiry(
                max_access_count=10,
            )
            .build()
        )

        self.mongodb.insert_link_record(link_record)

        expired_link_records = self.mongodb.find_expired_link_records()

        assert len(expired_link_records) == 1
        assert link_record == expired_link_records[0]
