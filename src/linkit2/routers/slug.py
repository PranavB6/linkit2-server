from fastapi import APIRouter, Depends
from pydantic import BaseModel

from linkit2.dependencies import get_mongodb
from linkit2.linkit_logging.linkit_logger import get_linkit_logger
from linkit2.mongodb import MongoDB

logger = get_linkit_logger()

router = APIRouter()


class GetAvailableSlugResponseBody(BaseModel):
    slug: str


@router.get("/slug")
async def get_available_slug(
    mongodb: MongoDB = Depends(get_mongodb),
) -> GetAvailableSlugResponseBody:
    available_slug = mongodb.get_available_slug()

    return GetAvailableSlugResponseBody.model_validate({"slug": available_slug})
