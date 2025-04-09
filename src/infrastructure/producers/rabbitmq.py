import aio_pika
import orjson
from aio_pika.abc import AbstractRobustConnection, AbstractRobustChannel, AbstractExchange

from domain.events.base import BaseEvent
from infrastructure.producers.base import BaseProducer
from settings.config import settings


class RabbitMQProducer(BaseProducer):
    connection: AbstractRobustConnection
    channel: AbstractRobustChannel
    exchange: AbstractExchange

    async def start(self):
        self.connection = await aio_pika.connect_robust(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            login=settings.RABBITMQ_USER,
            password=settings.RABBITMQ_PASSWORD,
            virtual_host=settings.RABBITMQ_VHOST,
        )
        self.channel = await self.connection.channel()
        self.exchange = await self.channel.get_exchange(name=settings.NANOSERVICES_EXCH_NAME)

    async def stop(self):
        if self.channel:
            await self.channel.close()
        if self.connection:
            await self.connection.close()

    async def publish(self, event: BaseEvent, topic: str):
        if not self.connection or not self.exchange:
            await self.start()

        await self.exchange.publish(
            aio_pika.Message(
                body=orjson.dumps(event.__dict__),
                content_type='application/json',
            ),
            routing_key=topic,
        )
