from linkit2.linkit_settings import get_linkit_settings
from linkit2.mongodb import MongoDB


def get_mongodb():
    linkit_settings = get_linkit_settings()
    mongodb = MongoDB(linkit_settings.mongodb)

    return mongodb
