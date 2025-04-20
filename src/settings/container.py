from functools import lru_cache

from punq import Container, Scope

from application.external_events.consumers.base import BaseConsumer
from application.external_events.consumers.rabbitmq import RabbitMQConsumer
from application.external_events.handlers.base import BaseExternalEventHandler
from application.external_events.handlers.notifications import UserRegistrationCompletedExternalEventHandler
from domain.commands.base import BaseCommand
from domain.commands.notifications import SendEmailNotificationCommand, SendSMSNotificationCommand
from domain.events.base import BaseEvent
from infrastructure.producers.base import BaseProducer
from infrastructure.producers.rabbitmq import RabbitMQProducer
from infrastructure.repositories.base import BaseNotificationRepository
from infrastructure.repositories.mongodb import BeanieNotificationRepository
from service.handlers.command.base import BaseCommandHandler
from service.handlers.command.notifications import SendEmailNotificationCommandHandler, SendSMSNotificationCommandHandler
from service.handlers.event.base import BaseEventHandler
from service.message_bus import MessageBus
from settings.config import Settings, settings


@lru_cache(1)
def initialize_container() -> Container:
    return _initialize_container()


def _initialize_container() -> Container:
    container = Container()

    def get_commands_map(repo: BaseNotificationRepository) -> dict[type[BaseCommand], BaseCommandHandler]:
        send_email_notification_handler = SendEmailNotificationCommandHandler(repo=repo)
        send_sms_notification_handler = SendSMSNotificationCommandHandler(repo=repo)

        commands_map = {
            SendEmailNotificationCommand: send_email_notification_handler,
            SendSMSNotificationCommand: send_sms_notification_handler,
        }
        return commands_map

    def get_events_map(producer: BaseProducer) -> dict[type[BaseEvent], list[BaseEventHandler]]:
        events_map = {}
        return events_map

    def get_external_events_map(bus: MessageBus) -> dict[str, BaseExternalEventHandler]:
        user_credentials_created_handler = UserRegistrationCompletedExternalEventHandler(bus=bus)

        external_events_map = {
            'user.registration.completed': user_credentials_created_handler,
        }
        return external_events_map

    def initialize_notification_beanie_db_repo() -> BaseNotificationRepository:
        return BeanieNotificationRepository()

    def initialize_message_bus() -> MessageBus:
        repo = container.resolve(BaseNotificationRepository)
        producer = container.resolve(BaseProducer)

        bus = MessageBus(
            repo=repo,
            commands_map=get_commands_map(repo=repo),
            events_map=get_events_map(producer=producer),
        )
        return bus

    def initialize_consumer() -> BaseConsumer:
        bus = container.resolve(MessageBus)
        return RabbitMQConsumer(external_events_map=get_external_events_map(bus))

    def initialize_producer() -> BaseProducer:
        return RabbitMQProducer()

    container.register(Settings, instance=settings, scope=Scope.singleton)
    container.register(BaseNotificationRepository, factory=initialize_notification_beanie_db_repo)
    container.register(MessageBus, factory=initialize_message_bus)
    container.register(BaseConsumer, factory=initialize_consumer, scope=Scope.singleton)
    container.register(BaseProducer, factory=initialize_producer, scope=Scope.singleton)

    return container
