import orjson
import pytest

from tests.fakes import FakeEvent


@pytest.mark.asyncio
class TestRabbitMQProducer:
    @pytest.mark.parametrize(
        'event',
        [
            (FakeEvent()),
        ],
    )
    async def test_producer(self, event, rabbitmq_consumer, rabbitmq_producer):
        assert rabbitmq_consumer.connection is not None
        assert rabbitmq_producer.connection is not None

        await rabbitmq_producer.publish(event=event, topic='fake.notification.topic')
        messages = []
        async with rabbitmq_consumer.queue.iterator() as queue_iterator:
            async for message in queue_iterator:
                async with message.process():
                    messages.append(message)
                    if queue_iterator._queue.empty():
                        break

        assert len(messages) == 1
        consumed_message = orjson.loads(messages[0].body)
        assert consumed_message == orjson.loads(orjson.dumps(event.__dict__))
        assert consumed_message['event_id'] == str(event.event_id)
