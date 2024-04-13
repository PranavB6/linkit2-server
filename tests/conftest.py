import os

import pytest

from linkit2.linkit_config import LinkitEnvironment, get_linkit_config
from linkit2.linkit_logging.linkit_logger import setup_logging


def pytest_sessionstart(session: pytest.Session):
    print("Session starting...")
    os.environ["LINKIT_ENVIRONMENT"] = "test"
    os.environ["MONGODB_DATABASE_NAME"] = "test_database"
    os.environ["MONGODB_LINKS_COLLECTION_NAME"] = "test_links_collection"
    os.environ["MONGODB_LINK_STATISTICS_COLLECTION_NAME"] = (
        "test_link_statistics_collection"
    )

    config = get_linkit_config()

    assert config.environment == LinkitEnvironment.TEST
    assert config.mongodb.database_name == "test_database"
    assert config.mongodb.links_collection_name == "test_links_collection"
    assert (
        config.mongodb.link_statistics_collection_name
        == "test_link_statistics_collection"
    )

    setup_logging()

    print("Setup Test Environment for Linkit")
