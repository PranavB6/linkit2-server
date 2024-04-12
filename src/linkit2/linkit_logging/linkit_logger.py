import logging
import logging.config
import logging.handlers
from pathlib import Path

import yaml


def setup_logging():
    logging_config_file = Path("src/linkit2/linkit_logging/logging_config.yaml")
    with open(logging_config_file, "r") as f:
        logging_config = yaml.safe_load(f)

    logging.config.dictConfig(logging_config)


def get_linkit_logger():
    return logging.getLogger("linkit2")


def get_mongodb_logger():
    return logging.getLogger("mongodb")
