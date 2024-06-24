import datetime
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from pydantic import BaseModel

from linkit2.linkit_logging.linkit_logger import get_linkit_logger, setup_logging
from linkit2.linkit_settings import get_linkit_settings
from linkit2.models.link_record import LinkRecord, LinkRecordInMongoDB
from linkit2.mongodb import MongoDB
from linkit2.utils import generate_slug, now

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


class ShortenLinkRequestBody(BaseModel):
    original_url: str


@app.post("/links")
async def shorten_link(
    body: ShortenLinkRequestBody, mongodb: MongoDB = Depends(get_mongodb)
) -> LinkRecordInMongoDB:
    new_slug = generate_slug()
    logger.debug(f"Generated new slug: '{new_slug}'")

    new_link_record = LinkRecord.model_validate(
        {
            "original_url": body.original_url,
            "slug": new_slug,
            "created_at": now(),
            "access": {
                "last_accessed_at": now(),
                "access_count": 0,
            },
            "expiry": {
                "expires_at": now() + datetime.timedelta(days=7),
                "max_access_count": 100,
            },
        }
    )

    inserted_id = mongodb.insert_link_record(new_link_record)

    link_record_in_mongodb = mongodb.find_link_record_with_id(inserted_id)

    assert link_record_in_mongodb is not None

    return link_record_in_mongodb


@app.get("/links/{slug}")
async def find_link_with_slug(
    slug: str, mongodb: MongoDB = Depends(get_mongodb)
) -> LinkRecordInMongoDB:
    link_record = mongodb.find_active_link_record_with_slug(slug)

    assert link_record is not None

    mongodb.process_link_record_access_with_id(link_record.id)

    updated_link_record = mongodb.find_link_record_with_id(link_record.id)

    assert updated_link_record is not None

    return updated_link_record


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
