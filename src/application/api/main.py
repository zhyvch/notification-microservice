import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from punq import Container

from application.external_events.consumers.base import BaseConsumer
from infrastructure.producers.base import BaseProducer
from infrastructure.storages.database import init_db
from settings.config import settings
from settings.container import initialize_container


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
        docs_url='/api/docs',
        debug=settings.NOTIFICATION_SERVICE_DEBUG,
        lifespan=lifespan,
    )
    # app.include_router(router, prefix='/notifications')

    return app