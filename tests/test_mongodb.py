import pytest
from linkit2.models.link_record import LinkRecord

from src.linkit2.linkit_config import get_linkit_config
from src.linkit2.mongodb import MongoDB


def setup_mongodb():
    config = get_linkit_config()
    mongodb = MongoDB(config.mongodb)
    return mongodb


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
        link_record = LinkRecord(url="https://www.google.com")
        inserted_id = mongodb.insert_link_record(link_record)
        assert inserted_id is not None

    def test_delete_database(self):
        mongodb = setup_mongodb()
        link_record = LinkRecord(url="https://www.google.com")
        mongodb.insert_link_record(link_record)

        mongodb.delete_database()

        records = mongodb.get_all_link_records()

        assert records is not None
        assert len(list(records)) == 0

    def test_get_link_record_by_id(self):
        mongodb = setup_mongodb()
        link_record = LinkRecord(url="https://pranav.com")
        inserted_id = mongodb.insert_link_record(link_record)

        record = mongodb.get_link_record_by_id(inserted_id)

        assert record is not None
        assert record.url == "https://pranav.com"
        assert record.id == inserted_id
