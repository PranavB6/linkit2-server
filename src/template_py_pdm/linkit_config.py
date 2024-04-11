from enum import Enum

from pydantic import Field
from pydantic_settings import BaseSettings


class LinkitEnvironment(str, Enum):
    PROD = "production"
    DEV = "development"
    TEST = "test"


class MongoDBConfig(BaseSettings):
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
    mongodb: MongoDBConfig


def get_linkit_config():
    # Initialize sub classes here
    # So that environment variables are read when in this function is called
    # Otherwise, the environment variables are read when the module is imported
    mongodb_config = MongoDBConfig()
    config = Settings(mongodb=mongodb_config)

    return config
