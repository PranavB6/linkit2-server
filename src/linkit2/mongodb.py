from typing import Any, Optional

from bson import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from linkit2.linkit_config import MongoDBConfig
from linkit2.linkit_logging.linkit_logger import get_mongodb_logger
from linkit2.models.link_record import LinkRecord, LinkRecordInMongoDB
from linkit2.models.link_statistics_record import LinkStatisticsRecord

logger = get_mongodb_logger()


class MongoDB:
    def __init__(self, mongodb_config: MongoDBConfig) -> None:
        self.mongodb_config = mongodb_config
        self.client = self._connect()
        self.database = self.client[mongodb_config.database_name]
        self.links_collection = self.database[mongodb_config.links_collection_name]
        self.link_statistics_collection = self.database[
            mongodb_config.link_statistics_collection_name
        ]

    def _connect(self):
        server_api = ServerApi("1", deprecation_errors=True)
        client = MongoClient(
            self.mongodb_config.connection_string,
            server_api=server_api,
            document_class=dict[str, Any],
        )

        try:
            client.admin.command("ping")
            logger.info("Successfully connected to MongoDB!")
        except Exception:
            logger.exception("Failed to connect to MongoDB!")

        return client

    def test_connection(self):
        response = self.client.admin.command("ping")
        assert response is not None
        assert response["ok"] == 1

    # --- Link Records ---

    def get_all_link_records(self) -> list[LinkRecordInMongoDB]:
        raw_records = list(self.links_collection.find())
        records = [LinkRecordInMongoDB(**record) for record in raw_records]

        return records

    def get_link_record_by_id(self, id: str) -> Optional[LinkRecordInMongoDB]:
        record = self.links_collection.find_one({"_id": ObjectId(id)})

        if record is None:
            return None

        return LinkRecordInMongoDB(**record)

    def insert_link_record(self, record: LinkRecord) -> str:
        inserted = self.links_collection.insert_one(record.model_dump())

        return str(inserted.inserted_id)

    # --- Link Statistics Records ---

    def get_all_link_statistics_records(self) -> list[LinkStatisticsRecord]:
        raw_records = list(self.link_statistics_collection.find())
        records = [LinkStatisticsRecord(**record) for record in raw_records]

        return records

    def get_link_statistics_record_by_id(
        self, id: str
    ) -> Optional[LinkStatisticsRecord]:
        record = self.link_statistics_collection.find_one({"_id": ObjectId(id)})

        if record is None:
            return None

        return LinkStatisticsRecord(**record)

    def insert_link_statistics_record(self, record: LinkStatisticsRecord) -> str:
        record_dict = record.model_dump()
        record_dict["link_record_id"] = ObjectId(record.link_record_id)
        inserted = self.link_statistics_collection.insert_one(record_dict)

        return str(inserted.inserted_id)

    def delete_database(self):
        self.client.drop_database(self.database.name)
