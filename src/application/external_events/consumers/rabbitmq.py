import logging
from dataclasses import dataclass, field

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


logger = logging.getLogger(__name__)


@dataclass
class RabbitMQConsumer(BaseConsumer):
    host: str
    port: int
    login: str
    password: str
    virtual_host: str
    exchange_name: str
    queue_name: str
    consuming_topics: list[str] = field(default_factory=list)
    connection: AbstractRobustConnection | None = None
    channel: AbstractRobustChannel | None = None
    exchange: AbstractRobustExchange | None = None
    queue: AbstractRobustQueue | None = None

    async def start(self):
        self.connection = await connect_robust(
            host=self.host,
            port=self.port,
            login=self.login,
            password=self.password,
            virtual_host=self.virtual_host,
        )
        self.channel = await self.connection.channel()
        self.exchange = await self.channel.declare_exchange(
            self.exchange_name,
            ExchangeType.TOPIC,
            durable=True,
        )
        self.queue = await self.channel.declare_queue(
            self.queue_name,
            durable=True,
        )
        for key in self.consuming_topics:
            await self.queue.bind(self.exchange, routing_key=key)
            logger.info(
                'Queue %(queue)s bound to routing key %(routing_key)s.',
                {
                    'queue': self.queue.name,
                    'routing_key': key,
                },
            )

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
            handler = self.external_events_map.get(message.routing_key)
            await handler(orjson.loads(message.body)) if handler else (
                logger.info('No handler found for message with routing key: %s', message.routing_key)
            )
        except Exception as e:
            logger.exception(
                'Error processing message(%(body)s)',
                {'body': message.body},
                exc_info=e,
            )
