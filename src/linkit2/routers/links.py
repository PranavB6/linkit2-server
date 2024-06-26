import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from linkit2.dependencies import get_mongodb
from linkit2.linkit_logging.linkit_logger import get_linkit_logger
from linkit2.models.link_record import LinkRecord, LinkRecordInMongoDB
from linkit2.mongodb import MongoDB
from linkit2.utils import generate_random_slug, now

logger = get_linkit_logger()

router = APIRouter()


class ShortenLinkRequestBody(BaseModel):
    original_url: str


@router.post("/links")
async def shorten_link(
    body: ShortenLinkRequestBody, mongodb: MongoDB = Depends(get_mongodb)
) -> LinkRecordInMongoDB:
    new_slug = generate_random_slug()
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


@router.get("/links/{slug}")
async def find_link_with_slug(
    slug: str, mongodb: MongoDB = Depends(get_mongodb)
) -> LinkRecordInMongoDB:
    link_record = mongodb.find_active_link_record_with_slug(slug)

    assert link_record is not None

    mongodb.process_link_record_access_with_id(link_record.id)

    updated_link_record = mongodb.find_link_record_with_id(link_record.id)

    assert updated_link_record is not None

    return updated_link_record
