import os

import pytest

from linkit2.linkit_config import LinkitEnvironment, get_linkit_config
from linkit2.linkit_logging.linkit_logger import setup_logging


def pytest_sessionstart(session: pytest.Session):
    print("Session starting...")
    os.environ["LINKIT_ENVIRONMENT"] = "test"
    os.environ["MONGODB_DATABASE_NAME"] = "test_database"
    os.environ["MONGODB_COLLECTION_NAME"] = "test_collection"

    config = get_linkit_config()

    assert config.environment == LinkitEnvironment.TEST
    assert config.mongodb.database_name == "test_database"
    assert config.mongodb.collection_name == "test_collection"

    setup_logging()

    print("Setup Test Environment for Linkit")
