from contextlib import asynccontextmanager

from faker import Faker
from fastapi import Depends, FastAPI

from linkit2.linkit_logging.linkit_logger import get_linkit_logger, setup_logging
from linkit2.linkit_settings import get_linkit_settings
from linkit2.mongodb import MongoDB

setup_logging()
logger = get_linkit_logger()


def get_mongodb():
    linkit_settings = get_linkit_settings()
    mongodb = MongoDB(linkit_settings.mongodb)

    return mongodb


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.debug("Application startup event")

    yield

    logger.debug("Application shutdown event")

    mongodb = get_mongodb()
    mongodb.close()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health/live")
async def check_health_live():
    return {"status": "LIVE"}


@app.get("/health/db")
async def check_health_mongodb(mongodb: MongoDB = Depends(get_mongodb)):
    return mongodb.get_health()


@app.post("/links")
async def shorten_link(mongodb: MongoDB = Depends(get_mongodb)) -> None:
    new_slug = Faker().pystr_format(
        string_format="?????", letters="abcdefghijklmnopqrstuvwxyz"
    )

    logger.debug(f"Generated new slug: {new_slug}")

    link_records = mongodb.get_all_link_records()

    logger.debug(link_records)

    return
