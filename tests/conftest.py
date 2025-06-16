import logging
from random import randint
from uuid import uuid4

import pytest
import pytest_asyncio

from beanie import init_beanie
from beanie.executors.migrate import run_migrate, MigrationSettings, RunningDirections

from motor.motor_asyncio import AsyncIOMotorClient

from application.external_events.consumers.rabbitmq import RabbitMQConsumer
from domain.entities.notifications import EmailNotificationEntity, SMSNotificationEntity
from domain.value_objects.notifications import PhoneNumberVO, EmailVO
from infrastructure.models.notifications import NotificationModel, NotificationTemplateModel
from infrastructure.producers.rabbitmq import RabbitMQProducer
from infrastructure.repositories.mongodb import BeanieNotificationRepository, BeanieNotificationTemplateRepository
from infrastructure.senders.email.smtp import SMTPEmailSender
from infrastructure.senders.sms.twilio import TwilioSMSSender
from service.message_bus import MessageBus
from settings.container import get_external_events_map, get_commands_map, get_events_map
from tests.config import test_settings
from tests.fakes import (
    FakeNotificationRepository,
    FakeNotificationTemplateRepository,
    FakeEmailSender,
    FakeSMSSender,
    FakeProducer,
    FakeConsumer,
)

logger = logging.getLogger(__name__)


SKIP_DIRS = {'e2e', 'integration'}

def pytest_addoption(parser):
    parser.addoption(
        '--run-all',
        action='store_true',
        default=False,
        help='run all tests'
    )

def pytest_ignore_collect(collection_path, config):
    if not config.getoption('--run-all') and collection_path.name in SKIP_DIRS:
        return True
    return None


@pytest_asyncio.fixture(scope='session')
async def mobgodb_db():
    client = AsyncIOMotorClient(test_settings.TESTS_MONGODB_URL)

    await init_beanie(
        database=client[test_settings.TESTS_MONGODB_DB],
        document_models=[NotificationModel, NotificationTemplateModel]
    )

    await run_migrate(
        settings=MigrationSettings(
            direction=RunningDirections.FORWARD,
            connection_uri=f'mongodb://{test_settings.TESTS_MONGODB_USER}:{test_settings.TESTS_MONGODB_PASSWORD}@{test_settings.TESTS_MONGODB_HOST}',
            database_name=test_settings.TESTS_MONGODB_DB,
            path='src/infrastructure/migrations/',
        )
    )


@pytest.fixture
def beanie_notification_repository():
    return BeanieNotificationRepository()


@pytest.fixture
def beanie_notification_template_repository():
    return BeanieNotificationTemplateRepository()


@pytest.fixture
def smtp_email_sender():
    return SMTPEmailSender(
        host=test_settings.TESTS_SMTP_HOST,
        port=test_settings.TESTS_SMTP_PORT,
        username=test_settings.TESTS_SMTP_USER,
        password=test_settings.TESTS_SMTP_PASSWORD,
        use_tls=test_settings.TESTS_SMTP_USE_TLS,
        use_ssl=test_settings.TESTS_SMTP_USE_SSL,
    )


@pytest.fixture
def twilio_sms_sender():
    return TwilioSMSSender(
        account_sid=test_settings.TESTS_TWILIO_ACCOUNT_SID,
        auth_token=test_settings.TESTS_TWILIO_AUTH_TOKEN,
    )


@pytest.fixture
def message_bus(
    beanie_notification_template_repository,
    beanie_notification_repository,
    smtp_email_sender,
    twilio_sms_sender,
    rabbitmq_producer
):
    bus = MessageBus(
        repo=beanie_notification_repository,
        commands_map=get_commands_map(
            email_sender=smtp_email_sender,
            sms_sender=twilio_sms_sender,
            notification_template_repo=beanie_notification_template_repository,
            notification_repo=beanie_notification_repository,
        ),
        events_map=get_events_map(producer=rabbitmq_producer),
    )
    return bus


@pytest_asyncio.fixture
async def rabbitmq_producer():
    producer = RabbitMQProducer(
        host=test_settings.TESTS_RABBITMQ_HOST if test_settings.DOCKER_RUN else '127.0.0.1',
        port=test_settings.TESTS_RABBITMQ_PORT if not test_settings.DOCKER_RUN else '5432',
        login=test_settings.TESTS_RABBITMQ_USER,
        password=test_settings.TESTS_RABBITMQ_PASSWORD,
        virtual_host=test_settings.TESTS_RABBITMQ_VHOST,
        exchange_name=test_settings.TESTS_NANOSERVICES_EXCH_NAME,
    )
    await producer.start()
    yield producer
    await producer.stop()


@pytest_asyncio.fixture
async def rabbitmq_consumer(message_bus):
    consumer = RabbitMQConsumer(
        host=test_settings.TESTS_RABBITMQ_HOST if test_settings.DOCKER_RUN else '127.0.0.1',
        port=test_settings.TESTS_RABBITMQ_PORT if not test_settings.DOCKER_RUN else '5432',
        login=test_settings.TESTS_RABBITMQ_USER,
        password=test_settings.TESTS_RABBITMQ_PASSWORD,
        virtual_host=test_settings.TESTS_RABBITMQ_VHOST,
        queue_name=test_settings.TESTS_NOTIFICATION_SERVICE_QUEUE_NAME,
        exchange_name=test_settings.TESTS_NANOSERVICES_EXCH_NAME,
        consuming_topics=test_settings.TESTS_NOTIFICATION_SERVICE_CONSUMING_TOPICS,
        external_events_map=get_external_events_map(bus=message_bus),
    )
    await consumer.start()

    if consumer.queue:
        await consumer.queue.purge()

    yield consumer
    await consumer.stop()


@pytest.fixture
def random_email_notification_entity():
    return EmailNotificationEntity(
        sender=EmailVO(test_settings.TESTS_FROM_EMAIL),
        receivers=[EmailVO(f'user_{uuid4()}@example.com'),],
        subject='Test Email Subject',
        text='Test Email Body',
        html='<p>Test Email Body</p>',
    )


@pytest.fixture
def random_sms_entity():
    return SMSNotificationEntity(
        sender=PhoneNumberVO(test_settings.TESTS_FROM_PHONE_NUMBER),
        receivers=[PhoneNumberVO(f'+{randint(1000000000, 9999999999)}'),],
        text='Test SMS Body',
    )


@pytest.fixture
def fake_notification_repository():
    return FakeNotificationRepository()


@pytest.fixture
def fake_notification_template_repository():
    templates = [
        {
            'name': 'registration_successful',
            'text_template': 'Dear %(first_name)s %(last_name)s %(middle_name)s we glad to inform you that your registration was successful!',
            'html_template': 'Dear <strong>%(first_name)s %(last_name)s %(middle_name)s</strong> we glad to inform you that your registration was successful!'
        },
        {
            'name': 'registration_failed',
            'text_template': 'Dear %(first_name)s %(last_name)s %(middle_name)s we sorry to inform you that your registration was not successful!',
            'html_template': 'Dear <strong>%(first_name)s %(last_name)s %(middle_name)s</strong> we sorry to inform you that your registration was not successful!'
        },
        {
            'name': 'registration_pending',
            'text_template': 'Dear %(first_name)s %(last_name)s %(middle_name)s we inform you that your registration is pending.',
            'html_template': 'Dear <strong>%(first_name)s %(last_name)s %(middle_name)s</strong> we inform you that your registration is pending.'
        },
        {
            'name': 'email_update_initiated',
            'text_template': 'Dear user, your email update has been initiated. Please follow the this link (http://localhost:8001/api/v1/me/credentials/email/verify?token=%(verify_token)s) to complete the process.',
            'html_template': 'Dear <strong>user</strong>, your email update has been initiated. Please follow the this <a href="http://localhost:8001/api/v1/me/credentials/email/verify?token=%(verify_token)s">link</a> to complete the process.'
        },
        {
            'name': 'email_updated',
            'text_template': 'Dear user, your email was successfully updated to %(new_email)s.',
            'html_template': 'Dear <strong>user</strong>, your email was successfully updated to <strong>%(new_email)s</strong>.'
        },
        {
            'name': 'phone_number_update_initiated',
            'text_template': 'Dear user, your phone number update has been initiated. Please follow the this link (http://localhost:8001/api/v1/me/credentials/phone-number/verify?token=%(verify_token)s) to complete the process.',
            'html_template': None
        },
        {
            'name': 'phone_number_updated',
            'text_template': 'Dear user, your phone number was successfully updated to %(new_phone_number)s.',
            'html_template': None
        },
        {
            'name': 'password_reset_initiated',
            'text_template': 'Dear user, your password reset has been initiated. Please follow the this link (http://localhost:8001/api/v1/password/reset?token=%(verify_token)s) to complete the process.',
            'html_template': 'Dear <strong>user</strong>, your password reset has been initiated. Please follow the this <a href="http://localhost:8001/api/v1/password/reset?token=%(verify_token)s">link</a> to complete the process.'
        },
    ]
    repo = FakeNotificationTemplateRepository()
    repo.templates_list.extend(templates)
    return repo


@pytest.fixture
def fake_email_sender():
    return FakeEmailSender()


@pytest.fixture
def fake_sms_sender():
    return FakeSMSSender()


@pytest.fixture
def fake_message_bus(
    fake_notification_repository,
    fake_notification_template_repository,
    fake_email_sender,
    fake_sms_sender,
    fake_producer,
):
    bus = MessageBus(
        repo=fake_notification_repository,
        commands_map=get_commands_map(
            email_sender=fake_email_sender,
            sms_sender=fake_sms_sender,
            notification_template_repo=fake_notification_template_repository,
            notification_repo=fake_notification_repository,
        ),
        events_map=get_events_map(producer=fake_producer),
    )
    return bus


@pytest.fixture
def fake_producer():
    return FakeProducer()


@pytest.fixture()
def fake_consumer(fake_message_bus):
    consumer = FakeConsumer(
        topics_to_consume=test_settings.TESTS_NOTIFICATION_SERVICE_CONSUMING_TOPICS,
        external_events_map=get_external_events_map(bus=fake_message_bus),
    )
    return consumer
