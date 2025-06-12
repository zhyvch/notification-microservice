from functools import lru_cache

from punq import Container, Scope

from application.external_events.consumers.base import BaseConsumer
from application.external_events.consumers.rabbitmq import RabbitMQConsumer
from application.external_events.handlers.base import BaseExternalEventHandler
from application.external_events.handlers.notifications import (
    UserRegistrationCompletedExternalEventHandler,
    UserEmailUpdateInitiatedExternalEventHandler,
    UserPhoneNumberUpdateInitiatedExternalEventHandler,
    UserPasswordResetInitiatedExternalEventHandler,
    UserEmailUpdatedExternalEventHandler,
    UserPhoneNumberUpdatedExternalEventHandler,
)
from domain.commands.base import BaseCommand
from domain.commands.notifications import (
    SendUserRegistrationCompletedMessageCommand,
    SendUserEmailUpdateInitiatedMessageCommand,
    SendUserPhoneNumberUpdateInitiatedMessageCommand,
    SendUserPasswordResetInitiatedMessageCommand,
    SendUserEmailUpdatedMessageCommand,
    SendUserPhoneNumberUpdatedMessageCommand,
)
from domain.events.base import BaseEvent
from infrastructure.producers.base import BaseProducer
from infrastructure.producers.rabbitmq import RabbitMQProducer
from infrastructure.repositories.base import BaseNotificationRepository, BaseNotificationTemplateRepository
from infrastructure.repositories.mongodb import BeanieNotificationRepository, BeanieNotificationTemplateRepository
from infrastructure.senders.email.base import BaseEmailSender
from infrastructure.senders.email.smtp import SMTPEmailSender
from infrastructure.senders.sms.base import BaseSMSSender
from infrastructure.senders.sms.twilio import TwilioSMSSender
from service.handlers.command.base import BaseCommandHandler
from service.handlers.command.notifications import (
    SendUserRegistrationCompletedMessageCommandHandler,
    SendUserEmailUpdateInitiatedMessageCommandHandler,
    SendUserPhoneNumberUpdateInitiatedMessageCommandHandler,
    SendUserPasswordResetInitiatedMessageCommandHandler,
    SendUserEmailUpdatedMessageCommandHandler,
    SendUserPhoneNumberUpdatedMessageCommandHandler,
)
from service.handlers.event.base import BaseEventHandler
from service.message_bus import MessageBus
from settings.config import Settings, settings


def get_commands_map(
    notification_template_repo: BaseNotificationTemplateRepository,
    notification_repo: BaseNotificationRepository,
    email_sender: BaseEmailSender,
    sms_sender: BaseSMSSender,
) -> dict[type[BaseCommand], BaseCommandHandler]:
    send_user_registration_completed_message_handler = SendUserRegistrationCompletedMessageCommandHandler(
        notification_template_repo=notification_template_repo,
        notification_repo=notification_repo,
        email_sender=email_sender,
        sms_sender=sms_sender,
    )
    send_user_email_update_initiated_message_handler = SendUserEmailUpdateInitiatedMessageCommandHandler(
        notification_template_repo=notification_template_repo,
        notification_repo=notification_repo,
        email_sender=email_sender,
    )
    send_user_phone_number_update_initiated_message_handler = SendUserPhoneNumberUpdateInitiatedMessageCommandHandler(
        notification_template_repo=notification_template_repo,
        notification_repo=notification_repo,
        sms_sender=sms_sender,
    )
    send_user_password_reset_initiated_message_handler = SendUserPasswordResetInitiatedMessageCommandHandler(
        notification_template_repo=notification_template_repo,
        notification_repo=notification_repo,
        email_sender=email_sender,
        sms_sender=sms_sender,
    )
    send_user_email_updated_message_handler = SendUserEmailUpdatedMessageCommandHandler(
        notification_template_repo=notification_template_repo,
        notification_repo=notification_repo,
        email_sender=email_sender,
    )
    send_user_phone_number_updated_message_handler = SendUserPhoneNumberUpdatedMessageCommandHandler(
        notification_template_repo=notification_template_repo,
        notification_repo=notification_repo,
        sms_sender=sms_sender,
    )

    commands_map = {
        SendUserRegistrationCompletedMessageCommand: send_user_registration_completed_message_handler,
        SendUserEmailUpdateInitiatedMessageCommand: send_user_email_update_initiated_message_handler,
        SendUserPhoneNumberUpdateInitiatedMessageCommand: send_user_phone_number_update_initiated_message_handler,
        SendUserPasswordResetInitiatedMessageCommand: send_user_password_reset_initiated_message_handler,
        SendUserEmailUpdatedMessageCommand: send_user_email_updated_message_handler,
        SendUserPhoneNumberUpdatedMessageCommand: send_user_phone_number_updated_message_handler,
    }
    return commands_map


def get_events_map(
    producer: BaseProducer,
) -> dict[type[BaseEvent], list[BaseEventHandler]]:
    events_map = {}
    return events_map


def get_external_events_map(bus: MessageBus) -> dict[str, BaseExternalEventHandler]:
    user_registration_completed_handler = UserRegistrationCompletedExternalEventHandler(bus=bus)
    user_email_update_initiated_handler = UserEmailUpdateInitiatedExternalEventHandler(bus=bus)
    user_phone_number_update_initiated_handler = UserPhoneNumberUpdateInitiatedExternalEventHandler(bus=bus)
    user_password_reset_initiated_handler = UserPasswordResetInitiatedExternalEventHandler(bus=bus)
    user_email_updated_handler = UserEmailUpdatedExternalEventHandler(bus=bus)
    user_phone_number_updated_handler = UserPhoneNumberUpdatedExternalEventHandler(bus=bus)

    external_events_map = {
        'user.registration.completed': user_registration_completed_handler,
        'user.email.update.initiated': user_email_update_initiated_handler,
        'user.phone_number.update.initiated': user_phone_number_update_initiated_handler,
        'user.password.reset.initiated': user_password_reset_initiated_handler,
        'user.email.updated': user_email_updated_handler,
        'user.phone_number.updated': user_phone_number_updated_handler,
    }
    return external_events_map


def _initialize_container() -> Container:
    container = Container()

    def initialize_notification_template_beanie_db_repo() -> BaseNotificationTemplateRepository:
        return BeanieNotificationTemplateRepository()


    def initialize_notification_beanie_db_repo() -> BaseNotificationRepository:
        return BeanieNotificationRepository()


    def initialize_email_sender() -> BaseEmailSender:
        return SMTPEmailSender(
            host=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            use_tls=settings.SMTP_USE_TLS,
            use_ssl=settings.SMTP_USE_SSL,
        )


    def initialize_sms_sender() -> BaseSMSSender:
        return TwilioSMSSender(
            account_sid=settings.TWILIO_ACCOUNT_SID,
            auth_token=settings.TWILIO_AUTH_TOKEN,
        )


    def initialize_message_bus(
        notification_template_repo: BaseNotificationTemplateRepository = None,
        notification_repo: BaseNotificationRepository = None,
        email_sender: BaseEmailSender = None,
        sms_sender: BaseSMSSender = None,
        producer: BaseProducer = None
    ) -> MessageBus:
        if notification_template_repo is None:
            notification_template_repo = container.resolve(BaseNotificationTemplateRepository)

        if notification_repo is None:
            notification_repo = container.resolve(BaseNotificationRepository)

        if email_sender is None:
            email_sender = container.resolve(BaseEmailSender)

        if sms_sender is None:
            sms_sender = container.resolve(BaseSMSSender)

        if producer is None:
            producer = container.resolve(BaseProducer)

        bus = MessageBus(
            repo=notification_repo,
            commands_map=get_commands_map(
                notification_template_repo=notification_template_repo,
                notification_repo=notification_repo,
                email_sender=email_sender,
                sms_sender=sms_sender,
            ),
            events_map=get_events_map(
                producer=producer,
            ),
        )
        return bus


    def initialize_producer() -> BaseProducer:
        return RabbitMQProducer(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            login=settings.RABBITMQ_USER,
            password=settings.RABBITMQ_PASSWORD,
            virtual_host=settings.RABBITMQ_VHOST,
            exchange_name=settings.NANOSERVICES_EXCH_NAME,
        )


    def initialize_consumer(
        bus: MessageBus = None
    ) -> BaseConsumer:
        if bus is None:
            bus = container.resolve(MessageBus)

        return RabbitMQConsumer(
            external_events_map=get_external_events_map(bus),
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            login=settings.RABBITMQ_USER,
            password=settings.RABBITMQ_PASSWORD,
            virtual_host=settings.RABBITMQ_VHOST,
            queue_name=settings.NOTIFICATION_SERVICE_QUEUE_NAME,
            exchange_name=settings.NANOSERVICES_EXCH_NAME,
            consuming_topics=settings.NOTIFICATION_SERVICE_CONSUMING_TOPICS,
        )


    container.register(Settings, instance=settings, scope=Scope.singleton)
    container.register(BaseNotificationTemplateRepository, factory=initialize_notification_template_beanie_db_repo)
    container.register(BaseNotificationRepository, factory=initialize_notification_beanie_db_repo)
    container.register(BaseEmailSender, factory=initialize_email_sender, scope=Scope.singleton)
    container.register(BaseSMSSender, factory=initialize_sms_sender, scope=Scope.singleton)
    container.register(MessageBus, factory=initialize_message_bus)
    container.register(BaseProducer, factory=initialize_producer, scope=Scope.singleton)
    container.register(BaseConsumer, factory=initialize_consumer, scope=Scope.singleton)

    return container



@lru_cache(1)
def initialize_container() -> Container:
    return _initialize_container()
