from fastapi import APIRouter, Depends

from linkit2.dependencies import get_mongodb
from linkit2.mongodb import MongoDB

router = APIRouter(prefix="/health")


@router.get("/live")
async def check_health_live():
    return {"status": "LIVE"}


@router.get("/db")
async def check_health_mongodb(mongodb: MongoDB = Depends(get_mongodb)):
    return mongodb.get_health()
