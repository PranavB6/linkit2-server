import datetime

import pytest

from linkit2.link_record_builder import LinkRecordBuilder
from linkit2.linkit_settings import get_linkit_settings
from linkit2.mongodb import MongoDB


@pytest.mark.mongodb
class TestMongoDB:
    def setup_class(self):
        settings = get_linkit_settings()
        self.mongodb = MongoDB(settings.mongodb)

    def setup_method(self):
        self.mongodb.delete_database()

    def test_find_active_link_record(self):
        link_record = LinkRecordBuilder().build()

        inserted_id = self.mongodb.insert_link_record(link_record)

        active_link_record = self.mongodb.find_active_link_record_with_slug(
            link_record.slug
        )

        assert active_link_record is not None
        assert active_link_record.slug == link_record.slug
        assert active_link_record.id == inserted_id

    def test_find_active_link_record_with_expired_link_record(self):
        link_record = (
            LinkRecordBuilder()
            .with_expiry(
                expires_at=datetime.datetime.now() - datetime.timedelta(days=1),
            )
            .build()
        )

        self.mongodb.insert_link_record(link_record)

        active_link_record = self.mongodb.find_active_link_record_with_slug(
            link_record.slug
        )

        assert active_link_record is None

    def test_find_active_link_record_with_max_access_count_reached(self):
        link_record = (
            LinkRecordBuilder()
            .with_access(
                access_count=10,
            )
            .with_expiry(
                max_access_count=10,
            )
            .build()
        )

        self.mongodb.insert_link_record(link_record)

        active_link_record = self.mongodb.find_active_link_record_with_slug(
            link_record.slug
        )

        assert active_link_record is None

    def test_process_link_record_access(self):
        link_record = (
            LinkRecordBuilder()
            .with_access(access_count=0)
            .with_expiry(max_access_count=5)
            .build()
        )

        self.mongodb.insert_link_record(link_record)
        active_link_record = self.mongodb.find_active_link_record_with_slug(
            link_record.slug
        )

        assert active_link_record is not None

        for num_hits in range(1, 5):
            self.mongodb.process_link_record_access_with_id(active_link_record.id)
            active_link_record = self.mongodb.find_active_link_record_with_slug(
                link_record.slug
            )

            assert active_link_record is not None
            assert active_link_record.access.access_count == num_hits

        self.mongodb.process_link_record_access_with_id(active_link_record.id)
        active_link_record = self.mongodb.find_active_link_record_with_slug(
            link_record.slug
        )

        assert active_link_record is None
