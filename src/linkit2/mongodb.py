from typing import Any, Optional

from bson import CodecOptions, ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from linkit2.linkit_logging.linkit_logger import get_mongodb_logger
from linkit2.linkit_settings import MongoDBSettings
from linkit2.models.link_record import LinkRecord, LinkRecordInMongoDB
from linkit2.utils import now

logger = get_mongodb_logger()


class MongoDB:
    _instance = None

    def __new__(cls, mongodb_settings: MongoDBSettings):
        if cls._instance is None:
            cls._instance = super(MongoDB, cls).__new__(cls)
            cls._initialize(cls._instance, mongodb_settings)

        return cls._instance

    def _initialize(self, mongodb_settings: MongoDBSettings):
        self.mongodb_settings = mongodb_settings
        self.client = self._connect()
        self.database = self.client.get_database(self.mongodb_settings.database_name)
        self.collection = self.database.get_collection(
            self.mongodb_settings.collection_name,
            codec_options=CodecOptions(tz_aware=True),
        )

    def _connect(self):
        server_api = ServerApi("1", deprecation_errors=True)
        client = MongoClient(
            self.mongodb_settings.connection_string,
            server_api=server_api,
            document_class=dict[str, Any],
        )

        try:
            client.admin.command("ping")
            logger.info("Successfully connected to MongoDB!")
        except Exception:
            logger.exception("Failed to connect to MongoDB!")

        return client

    def get_all_link_records(self) -> list[LinkRecordInMongoDB]:
        raw_records = self.collection.find({})

        return [
            LinkRecordInMongoDB.model_validate(raw_record) for raw_record in raw_records
        ]

    def insert_link_record(self, link_record: LinkRecord) -> str:
        raw_record = link_record.model_dump()
        insert_result = self.collection.insert_one(raw_record)

        return str(insert_result.inserted_id)

    def find_link_record_with_id(self, id: str) -> Optional[LinkRecordInMongoDB]:
        raw_record = self.collection.find_one({"_id": ObjectId(id)})

        if raw_record is None:
            return None

        return LinkRecordInMongoDB.model_validate(raw_record)

    def find_link_record_with_slug(self, slug: str) -> Optional[LinkRecordInMongoDB]:
        raw_record = self.collection.find_one({"slug": slug})

        if raw_record is None:
            return None

        return LinkRecordInMongoDB.model_validate(raw_record)

    def find_active_link_record_with_slug(
        self, slug: str
    ) -> Optional[LinkRecordInMongoDB]:
        raw_record = self.collection.find_one(
            {
                "slug": slug,
                "expiry.expires_at": {"$gte": now()},
                "$expr": {"$gt": ["$expiry.max_access_count", "$access.access_count"]},
            }
        )

        if raw_record is None:
            return None

        return LinkRecordInMongoDB.model_validate(raw_record)

    def process_link_record_access_with_id(self, id: str) -> None:
        self.collection.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {"access.last_accessed_at": now()},
                "$inc": {"access.access_count": 1},
            },
        )

    def delete_link_record_with_id(self, id: str) -> None:
        self.collection.delete_one({"_id": ObjectId(id)})

    def delete_database(self):
        self.client.drop_database(self.database)
