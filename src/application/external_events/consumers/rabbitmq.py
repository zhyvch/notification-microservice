import orjson

from aio_pika import connect_robust
from aio_pika.abc import (
    AbstractRobustConnection,
    AbstractRobustChannel,
    AbstractRobustExchange,
    AbstractRobustQueue,
    AbstractIncomingMessage,
    ExchangeType
)

from application.external_events.consumers.base import BaseConsumer
from settings.config import settings


class RabbitMQConsumer(BaseConsumer):
    connection: AbstractRobustConnection
    channel: AbstractRobustChannel
    exchange: AbstractRobustExchange
    queue: AbstractRobustQueue

    async def start(self):
        self.connection = await connect_robust(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            login=settings.RABBITMQ_USER,
            password=settings.RABBITMQ_PASSWORD,
            virtual_host=settings.RABBITMQ_VHOST,
        )
        self.channel = await self.connection.channel()
        self.exchange = await self.channel.declare_exchange(
            settings.NANOSERVICES_EXCH_NAME,
            ExchangeType.TOPIC,
            durable=True,
        )
        self.queue = await self.channel.declare_queue(
            settings.USER_SERVICE_QUEUE_NAME,
            durable=True,
        )
        for key in settings.USER_SERVICE_CONSUMING_RKS:
            await self.queue.bind(self.exchange, routing_key=key)
            print(f'Queue "{self.queue.name}" bound to routing key "{key}".')

    async def stop(self):
        if self.channel:
            await self.channel.close()
        if self.connection:
            await self.connection.close()

    async def consume(self):
        if not self.connection:
            await self.start()

        async with self.queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    await self.process_message(message)

    async def process_message(self, message: AbstractIncomingMessage):
        try:
            await self.external_events_map[message.routing_key](orjson.loads(message.body))
        except Exception as e:
            print('Error processing message:', e)
