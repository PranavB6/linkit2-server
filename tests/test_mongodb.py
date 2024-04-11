import pytest

from src.template_py_pdm.linkit_config import get_linkit_config
from src.template_py_pdm.mongodb import MongoDB


class TestMongoDB:
    @pytest.fixture()
    def mongodb(self):
        config = get_linkit_config()
        mongodb = MongoDB(config.mongodb)
        return mongodb

    def test_connection(self, mongodb: MongoDB):
        assert mongodb is not None
        mongodb.test_connection()

    def test_get_link_records_with_empty_collection(self, mongodb: MongoDB):
        records = mongodb.get_link_records()
        assert records is not None
        assert len(list(records)) == 0
