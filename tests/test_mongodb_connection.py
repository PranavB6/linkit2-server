import pytest

from linkit2.linkit_config import get_linkit_config
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

    def test_connection(self):
        mongodb = setup_mongodb()
        assert mongodb is not None
        mongodb.test_connection()
