from fastapi import APIRouter, Depends

from linkit2.dependencies import get_mongodb
from linkit2.linkit_logging.linkit_logger import get_linkit_logger
from linkit2.models.link_record import LinkRecordInMongoDB
from linkit2.mongodb import MongoDB

logger = get_linkit_logger()

router = APIRouter()


@router.get("/statistics/links/{link_id}")
async def find_link_with_id(
    link_id: str, mongodb: MongoDB = Depends(get_mongodb)
) -> LinkRecordInMongoDB:
    link_record = mongodb.find_link_record_with_id(link_id)

    assert link_record is not None

    return link_record
