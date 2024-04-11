import os

import pytest

from src.template_py_pdm.linkit_config import LinkitEnvironment, get_linkit_config


def pytest_sessionstart(session: pytest.Session):
    print("Session starting...")
    os.environ["LINKIT_ENVIRONMENT"] = "test"
    os.environ["MONGODB_DATABASE_NAME"] = "test_database"
    os.environ["MONGODB_COLLECTION_NAME"] = "test_collection"

    config = get_linkit_config()

    assert config.environment == LinkitEnvironment.TEST
    assert config.mongodb.database_name == "test_database"
    assert config.mongodb.collection_name == "test_collection"

    print("Setup Test Environment for Linkit")
