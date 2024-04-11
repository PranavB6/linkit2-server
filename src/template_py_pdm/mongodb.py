from bson.raw_bson import RawBSONDocument
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from template_py_pdm.linkit_config import MongoDBConfig


class MongoDB:
    def __init__(self, mongodb_config: MongoDBConfig) -> None:
        self.mongodb_config = mongodb_config
        self.client = self._connect()
        self.links_database = self.client[mongodb_config.database_name]
        self.links_collection = self.links_database[mongodb_config.collection_name]

    def _connect(self):
        server_api = ServerApi("1", deprecation_errors=True)
        client = MongoClient(
            self.mongodb_config.connection_string,
            server_api=server_api,
            document_class=RawBSONDocument,
        )

        try:
            client.admin.command("ping")
            print("Successfully connected to MongoDB!")
        except Exception as e:
            print(e)

        return client

    def test_connection(self):
        response = self.client.admin.command("ping")
        assert response is not None
        assert response["ok"] == 1

    def get_link_records(self):
        return self.links_collection.find({})
