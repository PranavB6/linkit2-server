from contextlib import asynccontextmanager

from fastapi import FastAPI

from linkit2.linkit_logging.linkit_logger import get_linkit_logger, setup_logging
from linkit2.linkit_settings import get_linkit_settings
from linkit2.mongodb import MongoDB
from linkit2.routers import health, links, slug, statistics

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
app.include_router(statistics.router)
app.include_router(slug.router)
