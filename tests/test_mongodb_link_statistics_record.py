from datetime import datetime

import pytest
from bson.objectid import ObjectId

from linkit2.linkit_config import get_linkit_config
from linkit2.models.link_statistics_record import LinkStatisticsRecord
from linkit2.mongodb import MongoDB


# create external method because pytest fixures cannot be used in class setup_method
def setup_mongodb():
    config = get_linkit_config()
    mongodb = MongoDB(config.mongodb)
    return mongodb


@pytest.mark.mongodb
class TestMongoDB:
    def setup_method(self, test_method: pytest.Function):
        mongodb = setup_mongodb()
        mongodb.delete_database()

    def test_get_link_statistic_records_with_empty_collection(self):
        mongodb = setup_mongodb()
        records = mongodb.get_all_link_statistics_records()

        assert records is not None
        assert len(list(records)) == 0

    def test_insert_link_statistics_record(self):
        mongodb = setup_mongodb()
        link_statistics_record = LinkStatisticsRecord(
            **{
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
            }  # type: ignore
        )

        inserted_id = mongodb.insert_link_statistics_record(link_statistics_record)

        assert inserted_id is not None
