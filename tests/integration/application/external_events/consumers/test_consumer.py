import asyncio

import orjson
import pytest

from tests.fakes import FakeEvent, get_fake_external_events_map


@pytest.mark.asyncio
class TestRabbitMQConsumer:
    @pytest.mark.parametrize(
        'event',
        [
            (FakeEvent()),
        ],
    )
    async def test_consumer(self, event, rabbitmq_consumer, rabbitmq_producer):
        assert rabbitmq_consumer.connection is not None
        assert rabbitmq_producer.connection is not None

        rabbitmq_consumer.external_events_map = get_fake_external_events_map()
        await rabbitmq_producer.publish(event=event, topic='fake.notification.topic')
        consuming_task = asyncio.create_task(rabbitmq_consumer.consume())

        handler = rabbitmq_consumer.external_events_map.get('fake.notification.topic')
        retry_count = 0
        max_retries = 10
        while handler.body is None and retry_count < max_retries:
            await asyncio.sleep(0.1)
            retry_count += 1

        assert handler.body == orjson.loads(orjson.dumps(event.__dict__))

        consuming_task.cancel()
