import os

import pytest

from linkit2.linkit_logging.linkit_logger import get_linkit_logger, setup_logging
from linkit2.linkit_settings import LinkitEnvironment, get_linkit_settings

logger = get_linkit_logger()


def pytest_sessionstart(session: pytest.Session):
    setup_logging()

    logger.debug("Pytest session starting...")

    os.environ["LINKIT_ENVIRONMENT"] = "test"
    os.environ["MONGODB_DATABASE_NAME"] = "test_database"

    settings = get_linkit_settings()

    assert settings.environment == LinkitEnvironment.TEST
    assert settings.mongodb.database_name == "test_database"

    logger.debug("Completed setting up test environment")
