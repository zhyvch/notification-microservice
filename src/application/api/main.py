import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from punq import Container

from application.api.exception_handlers import exception_registry
from application.external_events.consumers.base import BaseConsumer
from infrastructure.producers.base import BaseProducer
from infrastructure.storages.database import init_db
from settings.config import settings
from settings.container import initialize_container


logging.basicConfig(
    level=settings.LOG_LEVEL,
    format=settings.LOG_FORMAT,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()

    container: Container = initialize_container()
    consumer: BaseConsumer = container.resolve(BaseConsumer)
    producer: BaseProducer = container.resolve(BaseProducer)

    await consumer.start()
    consume_task = asyncio.create_task(consumer.consume())

    await producer.start()

    yield

    await producer.stop()

    consume_task.cancel()
    await consumer.stop()


def create_app():
    app = FastAPI(
        title='Notification Service',
        description='Simple notification service',
        docs_url=settings.NOTIFICATION_SERVICE_API_DOCS_URL,
        debug=settings.NOTIFICATION_SERVICE_DEBUG,
        lifespan=lifespan,
        default_response_class=ORJSONResponse,
    )
    # app.include_router(router, prefix=settings.NOTIFICATION_SERVICE_API_PREFIX)
    exception_registry(app)

    return app