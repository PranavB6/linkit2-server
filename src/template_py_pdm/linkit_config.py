from enum import Enum

from pydantic import Field
from pydantic_settings import BaseSettings


class LinkitEnvironment(str, Enum):
    PROD = "production"
    DEV = "development"
    TEST = "test"


class Settings(BaseSettings):
    environment: LinkitEnvironment = Field(
        default=None, validation_alias="Linkit_Environment"
    )


def get_linkit_config():
    config = Settings()

    return config
