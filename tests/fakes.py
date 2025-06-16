import asyncio
import logging
from dataclasses import field, dataclass
from uuid import UUID

from application.external_events.consumers.base import BaseConsumer
from application.external_events.handlers.base import BaseExternalEventHandler
from domain.commands.base import BaseCommand
from domain.entities.notifications import EmailNotificationEntity, SMSNotificationEntity
from domain.events.base import BaseEvent
from infrastructure.exceptions.notifications import NotificationTemplateNotFoundException, NotificationNotFoundException
from infrastructure.producers.base import BaseProducer


from infrastructure.repositories.base import BaseNotificationRepository, BaseNotificationTemplateRepository
from infrastructure.senders.email.base import BaseEmailSender
from infrastructure.senders.sms.base import BaseSMSSender

logger = logging.getLogger(__name__)


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


@dataclass
class FakeNotificationRepository(BaseNotificationRepository):
    notifications_list: list[EmailNotificationEntity | SMSNotificationEntity] = field(default_factory=list)

    async def add(
        self,
        notification: EmailNotificationEntity | SMSNotificationEntity
    ) -> None:
        logger.debug('Adding notification with ID \'%s\'', notification.id)
        self.notifications_list.append(notification)

    async def get(
        self,
        notification_id: UUID,
    ) -> EmailNotificationEntity | SMSNotificationEntity:
        logger.debug('Fetching notification with ID \'%s\'', notification_id)
        for notification in self.notifications_list:
            if notification.id == notification_id:
                logger.debug('Notification found: %s', notification_id)
                return notification
        logger.warning('Notification not found: %s', notification_id)
        raise NotificationNotFoundException(notification_id=notification_id)


@dataclass
class FakeNotificationTemplateRepository(BaseNotificationTemplateRepository):
    templates_list: list[dict[str, str | None]] = field(default_factory=list)

    async def add(
        self,
        name: str,
        text_template: str,
        html_template: str | None = None,
    ) -> None:
        logger.debug('Adding notification template with name: %s', name)
        template = {
            'name': name,
            'text_template': text_template,
            'html_template': html_template
        }
        self.templates_list.append(template)

    async def get(
        self,
        name: str,
    ) -> dict[str, str]:
        logger.debug('Fetching notification template with name: %s', name)
        for template in self.templates_list:
            if template['name'] == name:
                logger.debug('Template found: %s', name)
                return template
        logger.warning('Template not found: %s', name)
        raise NotificationTemplateNotFoundException(name=name)


@dataclass
class FakeEmailSender(BaseEmailSender):
    async def send_targeted_email(
        self,
        sender: str,
        receiver: str,
        subject: str,
        text: str,
        html: str | None = None,
    ) -> None:
        logger.debug('Sending targeted email to %s with subject: %s', receiver, subject)
        await asyncio.sleep(0.1)
        logger.info('Email sent to %s with subject: %s;\ntext: %s', receiver, subject, text)

    async def send_mass_email(
        self,
        sender: str,
        receivers: list[str],
        subject: str,
        text: str,
        html: str | None = None,
    ) -> None:
        logger.debug('Sending mass email to %d receivers with subject: %s', len(receivers), subject)
        await asyncio.sleep(0.1)
        for receiver in receivers:
            logger.info('Email sent to %s with subject: %s;\ntext: %s', receiver, subject, text)


@dataclass
class FakeSMSSender(BaseSMSSender):
    async def send_targeted_sms(
        self,
        sender: str,
        receiver: str,
        text: str,
    ) -> None:
        logger.debug('Sending targeted SMS to %s', receiver)
        await asyncio.sleep(0.1)
        logger.info('SMS sent to %s with text: %s', receiver, text)

    async def send_mass_sms(
        self,
        sender: str,
        receivers: list[str],
        text: str,
    ) -> None:
        logger.debug('Sending mass SMS to %d receivers', len(receivers))
        await asyncio.sleep(0.1)
        for receiver in receivers:
            logger.info('SMS sent to %s with text: %s', receiver, text)


@dataclass
class FakeBroker(metaclass=SingletonMeta):
    queue: list = field(default_factory=list)


class FakeProducer(BaseProducer):
    broker = FakeBroker()

    async def start(self):
        logger.debug('Starting FakeProducer')
        pass

    async def stop(self):
        logger.debug('Stopping FakeProducer')
        pass

    async def publish(self, event: BaseEvent, topic: str):
        logger.debug('Publishing event to topic: %s', topic)
        self.broker.queue.append({'topic': topic, 'event': event.__class__.__name__, 'body': event.__dict__})


@dataclass
class FakeConsumer(BaseConsumer):
    broker: FakeBroker = field(default_factory=FakeBroker, kw_only=True)
    consuming_task: asyncio.Task | None = field(default=None, kw_only=True)
    topics_to_consume: list[str] = field(default_factory=list, kw_only=True)

    async def start(self):
        logger.debug('Starting FakeConsumer')
        if not self.consuming_task:
            logger.debug('Creating new consuming task')
            self.consuming_task = asyncio.create_task(self.consume())


    async def stop(self):
        logger.debug('Stopping FakeConsumer')
        if self.consuming_task:
            logger.debug('Cancelling consuming task')
            self.consuming_task.cancel()
            self.consuming_task = None


    async def consume(self):
        logger.debug('FakeConsumer consuming messages')
        while True:
            for m in self.broker.queue:
                if m['topic'] in self.topics_to_consume:
                    logger.debug('Processing message for topic: %s', m['topic'])
                    await self.external_events_map[m['topic']](m['body'])
                    self.broker.queue.remove(m)
                else:
                    logger.debug('Ignoring message for topic: %s', m['topic'])
            await asyncio.sleep(0.1)


class FakeCommand(BaseCommand):
    ...


class FakeEvent(BaseEvent):
    ...


class FakeExternalEventHandler(BaseExternalEventHandler):
    body = None

    async def __call__(self, body: dict) -> None:
        self.body = body
        logger.info('FakeExternalEventHandler called with body: %s', body)


def get_fake_external_events_map() -> dict[str, BaseExternalEventHandler]:
    fake_handler = FakeExternalEventHandler(bus=None)

    fake_external_events_map = {
        'fake.notification.topic': fake_handler,
    }
    return fake_external_events_map
