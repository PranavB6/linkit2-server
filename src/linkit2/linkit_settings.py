from enum import Enum

from pydantic import Field
from pydantic_settings import BaseSettings

from linkit2.linkit_logging.linkit_logger import get_linkit_logger

logger = get_linkit_logger()


class LinkitEnvironment(str, Enum):
    DEVELOPMENT = "development"
    TEST = "test"
    PRODUCTION = "production"


class MongoDBSettings(BaseSettings):
    connection_string: str = Field(
        default=None, validation_alias="MONGODB_CONNECTION_STRING"
    )
    database_name: str = Field(default=None, validation_alias="MONGODB_DATABASE_NAME")
    collection_name: str = Field(
        default=None, validation_alias="MONGODB_COLLECTION_NAME"
    )


class Settings(BaseSettings):
    environment: LinkitEnvironment = Field(
        default=None, validation_alias="LINKIT_ENVIRONMENT"
    )
    mongodb: MongoDBSettings = Field(default_factory=MongoDBSettings)


def get_linkit_settings() -> Settings:
    settings = Settings()

    logger.debug("Settings: %s", settings.model_dump_json())
    return Settings()
