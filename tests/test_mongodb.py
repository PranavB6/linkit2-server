import pytest
from bson import ObjectId

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

    def test_get_link_records_with_empty_db(self):
        link_records_mongodb = self.mongodb.get_all_link_records()

        assert len(link_records_mongodb) == 0

    def test_insert_link_record(self):
        link_record = LinkRecordBuilder().build()

        inserted_id = self.mongodb.insert_link_record(link_record)

        assert inserted_id is not None

    def test_insert_multiple_link_records(self):
        link_records = [LinkRecordBuilder().build() for _ in range(3)]

        inserted_ids = [
            self.mongodb.insert_link_record(link_record) for link_record in link_records
        ]

        assert all(inserted_ids)

    def test_find_link_record_with_id(self):
        link_record = LinkRecordBuilder().build()
        inserted_id = self.mongodb.insert_link_record(link_record)

        link_record_mongodb = self.mongodb.find_link_record_with_id(inserted_id)

        assert link_record == link_record_mongodb

    def test_find_link_record_with_id_with_empty_db(self):
        random_id = ObjectId()
        link_record_mongodb = self.mongodb.find_link_record_with_id(str(random_id))

        assert link_record_mongodb is None

    # def test_find_link_record_with_original_url_with_empty_db(self):
    #     pass

    # def test_delete_link_record(self):
    #     pass

    # def test_delete_link_record_with_empty_db(self):
    #     pass
