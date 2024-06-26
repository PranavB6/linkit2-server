from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from pydantic import BaseModel

from linkit2.linkit_logging.linkit_logger import get_linkit_logger, setup_logging
from linkit2.linkit_settings import get_linkit_settings
from linkit2.models.link_record import LinkRecordInMongoDB
from linkit2.mongodb import MongoDB
from linkit2.routers import health, links

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


app.include_router(health.router)
app.include_router(links.router)


@app.get("/statistics/links/{link_id}")
async def find_link_with_id(
    link_id: str, mongodb: MongoDB = Depends(get_mongodb)
) -> LinkRecordInMongoDB:
    link_record = mongodb.find_link_record_with_id(link_id)

    assert link_record is not None

    return link_record


class GetAvailableSlugResponseBody(BaseModel):
    slug: str


@app.get("/slug")
async def get_available_slug(
    mongodb: MongoDB = Depends(get_mongodb),
) -> GetAvailableSlugResponseBody:
    available_slug = mongodb.get_available_slug()

    return GetAvailableSlugResponseBody.model_validate({"slug": available_slug})
