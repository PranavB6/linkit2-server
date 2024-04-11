from enum import Enum

from pydantic import Field
from pydantic_settings import BaseSettings


class LinkitEnvironment(str, Enum):
    PROD = "production"
    DEV = "development"
    TEST = "test"


class Settings(BaseSettings):
    env: LinkitEnvironment = Field(validation_alias="Linkit_Environment", default=None)


def get_linkit_config():
    config = Settings()

    return config
