import bson.errors
import pytest
from bson.objectid import ObjectId
from linkit2.models.link_record import LinkRecord

from src.linkit2.linkit_config import get_linkit_config
from src.linkit2.mongodb import MongoDB


def setup_mongodb():
    config = get_linkit_config()
    mongodb = MongoDB(config.mongodb)
    return mongodb


@pytest.mark.mongodb
class TestMongoDB:
    def setup_method(self, test_method: pytest.Function):
        mongodb = setup_mongodb()
        mongodb.delete_database()

    def test_connection(self):
        mongodb = setup_mongodb()
        assert mongodb is not None
        mongodb.test_connection()

    def test_get_link_records_with_empty_collection(self):
        mongodb = setup_mongodb()
        records = mongodb.get_all_link_records()
        assert records is not None
        assert len(list(records)) == 0

    def test_insert_link_record(self):
        mongodb = setup_mongodb()
        link_record = LinkRecord(originalUrl="https://www.google.com")
        inserted_id = mongodb.insert_link_record(link_record)
        assert inserted_id is not None

    def test_delete_database(self):
        mongodb = setup_mongodb()
        link_record = LinkRecord(originalUrl="https://www.google.com")
        mongodb.insert_link_record(link_record)

        mongodb.delete_database()

        records = mongodb.get_all_link_records()

        assert records is not None
        assert len(list(records)) == 0

    def test_get_link_record_by_id(self):
        mongodb = setup_mongodb()
        link_record = LinkRecord(originalUrl="https://pranav.com")
        inserted_id = mongodb.insert_link_record(link_record)

        record = mongodb.get_link_record_by_id(inserted_id)

        assert record is not None
        assert record.originalUrl == "https://pranav.com"
        assert record.id == inserted_id

    def test_get_link_record_by_id_with_invalid_id(self):
        mongodb = setup_mongodb()
        with pytest.raises(bson.errors.InvalidId):
            mongodb.get_link_record_by_id("invalid_id")

    def test_get_link_record_by_id_with_non_existent_id(self):
        mongodb = setup_mongodb()
        random_object_id = str(ObjectId())
        record = mongodb.get_link_record_by_id(random_object_id)
        assert record is None

    def test_get_link_records_with_3_records(self):
        mongodb = setup_mongodb()
        link_record1 = LinkRecord(originalUrl="https://pranav.com")
        link_record2 = LinkRecord(originalUrl="https://google.com")
        link_record3 = LinkRecord(originalUrl="https://facebook.com")

        mongodb.insert_link_record(link_record1)
        mongodb.insert_link_record(link_record2)
        mongodb.insert_link_record(link_record3)

        records = mongodb.get_all_link_records()

        assert records is not None
        assert len(list(records)) == 3
        assert set([record.originalUrl for record in records]) == set(
            [
                record.originalUrl
                for record in [link_record1, link_record2, link_record3]
            ]
        )
