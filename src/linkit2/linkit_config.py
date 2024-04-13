from enum import Enum

from pydantic import Field
from pydantic_settings import BaseSettings


class LinkitEnvironment(str, Enum):
    PROD = "production"
    DEV = "development"
    TEST = "test"


class MongoDBConfig(BaseSettings):
    connection_string: str = Field(
        validation_alias="MONGODB_CONNECTION_STRING",
        default=None,
        validate_default=True,
    )
    database_name: str = Field(
        validation_alias="MONGODB_DATABASE_NAME", default=None, validate_default=True
    )
    links_collection_name: str = Field(
        validation_alias="MONGODB_LINKS_COLLECTION_NAME",
        default=None,
        validate_default=True,
    )
    link_statistics_collection_name: str = Field(
        validation_alias="MONGODB_LINK_STATISTICS_COLLECTION_NAME",
        default=None,
        validate_default=True,
    )


class Settings(BaseSettings):
    environment: LinkitEnvironment = Field(
        default=None, validation_alias="LINKIT_ENVIRONMENT"
    )
    mongodb: MongoDBConfig = Field(default_factory=MongoDBConfig)


def get_linkit_config():
    config = Settings()

    return config
