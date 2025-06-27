import string
import random
from contextlib import nullcontext as not_raises
from uuid import uuid4

import pytest


from application.external_events.handlers.notifications import (
    UserRegistrationCompletedExternalEventHandler,
    UserEmailUpdateInitiatedExternalEventHandler,
    UserPhoneNumberUpdateInitiatedExternalEventHandler,
    UserPasswordResetInitiatedExternalEventHandler,
    UserEmailUpdatedExternalEventHandler,
    UserPhoneNumberUpdatedExternalEventHandler,
)
from domain.commands.notifications import UserCredentialsStatus
from domain.entities.notifications import EmailNotificationEntity, SMSNotificationEntity
from domain.exceptions.notifications import InsufficientCredentialsInfoException
from domain.value_objects.notifications import EmailVO, PhoneNumberVO


@pytest.mark.asyncio
class TestExternalEventHandlers:
    @pytest.mark.parametrize(
        'body, expectation',
        [
            (
                {
                    'user_id': str(uuid4()),
                    'email': f'{''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(230))}@testmail.com',
                    'phone_number': f'+{''.join(random.choice(string.digits) for _ in range(14))}',
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'middle_name': 'A',
                    'credentials_status': UserCredentialsStatus.SUCCESS.value,
                }, not_raises()
            ),
            (
                {
                    'user_id': str(uuid4()),
                    'email': None,
                    'phone_number': f'+{''.join(random.choice(string.digits) for _ in range(14))}',
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'middle_name': 'A',
                    'credentials_status': UserCredentialsStatus.PENDING.value,
                }, not_raises()
            ),
            (
                {
                    'user_id': str(uuid4()),
                    'email': f'{''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(230))}@testmail.com',
                    'phone_number': None,
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'middle_name': 'A',
                    'credentials_status': UserCredentialsStatus.FAILED.value,
                }, not_raises()
            ),
            (
                {
                    'user_id': str(uuid4()),
                    'email': None,
                    'phone_number': None,
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'middle_name': 'A',
                    'credentials_status': UserCredentialsStatus.SUCCESS.value,
                }, pytest.raises(InsufficientCredentialsInfoException)
            ),
        ]
    )
    async def test_user_registration_completed_external_event_handler(
        self, mongodb_db, body, expectation, beanie_notification_repository, message_bus,
    ):
        message_bus.repo = beanie_notification_repository

        handler = UserRegistrationCompletedExternalEventHandler(bus=message_bus)
        with expectation:
            await handler(body)

            assert len(beanie_notification_repository.loaded_notifications) == 1
            notification = beanie_notification_repository.loaded_notifications.pop()
            assert len(notification.receivers) == 1
            receiver = notification.receivers[0]

            if body.get('email'):
                assert notification.__class__ is EmailNotificationEntity
                assert receiver == EmailVO(body['email'])
            elif body.get('phone_number'):
                assert notification.__class__ is SMSNotificationEntity
                assert receiver == PhoneNumberVO(body['phone_number'])


    @pytest.mark.parametrize(
        'body, expectation',
        [
            (
                {
                    'user_id': str(uuid4()),
                    'new_email': f'{''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(230))}@testmail.com',
                    'verification_token': 'some-verification-token',
                }, not_raises()
            ),
        ]
    )
    async def test_user_email_update_initiated_external_event_handler(
        self, mongodb_db, body, expectation, beanie_notification_repository, message_bus,
    ):
        message_bus.repo = beanie_notification_repository

        handler = UserEmailUpdateInitiatedExternalEventHandler(bus=message_bus)
        with expectation:
            await handler(body)

            assert len(beanie_notification_repository.loaded_notifications) == 1
            notification = beanie_notification_repository.loaded_notifications.pop()
            assert len(notification.receivers) == 1
            receiver = notification.receivers[0]
            assert notification.__class__ is EmailNotificationEntity
            assert receiver == EmailVO(body['new_email'])
            assert body['verification_token'] in notification.text and body['verification_token'] in notification.html


    @pytest.mark.parametrize(
        'body, expectation',
        [
            (
                {
                    'user_id': str(uuid4()),
                    'new_phone_number': f'+{''.join(random.choice(string.digits) for _ in range(14))}',
                    'verification_token': 'some-verification-token',
                }, not_raises()
            ),
        ]
    )
    async def test_user_phone_number_update_initiated_external_event_handler(
        self, mongodb_db, body, expectation, beanie_notification_repository, message_bus,
    ):
        message_bus.repo = beanie_notification_repository

        handler = UserPhoneNumberUpdateInitiatedExternalEventHandler(bus=message_bus)
        with expectation:
            await handler(body)

            assert len(beanie_notification_repository.loaded_notifications) == 1
            notification = beanie_notification_repository.loaded_notifications.pop()
            assert len(notification.receivers) == 1
            receiver = notification.receivers[0]
            assert notification.__class__ is SMSNotificationEntity
            assert receiver == PhoneNumberVO(body['new_phone_number'])
            assert body['verification_token'] in notification.text


    @pytest.mark.parametrize(
        'body, expectation',
        [
            (
                {
                    'user_id': str(uuid4()),
                    'email': f'{''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(230))}@testmail.com',
                    'phone_number': f'+{''.join(random.choice(string.digits) for _ in range(14))}',
                    'verification_token': 'some-verification-token',
                }, not_raises()
            ),
            (
                {
                    'user_id': str(uuid4()),
                    'email': None,
                    'phone_number': f'+{''.join(random.choice(string.digits) for _ in range(14))}',
                    'verification_token': 'some-verification-token',
                }, not_raises()
            ),
            (
                {
                    'user_id': str(uuid4()),
                    'email': f'{''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(230))}@testmail.com',
                    'phone_number': None,
                    'verification_token': 'some-verification-token',
                }, not_raises()
            ),
            (
                {
                    'user_id': str(uuid4()),
                    'email': None,
                    'phone_number': None,
                    'verification_token': 'some-verification-token',
                }, pytest.raises(InsufficientCredentialsInfoException)
            ),
        ]
    )
    async def test_user_password_reset_initiated_external_event_handler(
        self, mongodb_db, body, expectation, beanie_notification_repository, message_bus,
    ):
        message_bus.repo = beanie_notification_repository

        handler = UserPasswordResetInitiatedExternalEventHandler(bus=message_bus)
        with expectation:
            await handler(body)

            assert len(beanie_notification_repository.loaded_notifications) == 1
            notification = beanie_notification_repository.loaded_notifications.pop()
            assert len(notification.receivers) == 1
            receiver = notification.receivers[0]

            if body.get('email'):
                assert notification.__class__ is EmailNotificationEntity
                assert receiver == EmailVO(body['email'])
                assert body['verification_token'] in notification.text and body['verification_token'] in notification.html
            elif body.get('phone_number'):
                assert notification.__class__ is SMSNotificationEntity
                assert receiver == PhoneNumberVO(body['phone_number'])
                assert body['verification_token'] in notification.text


    @pytest.mark.parametrize(
        'body, expectation',
        [
            (
                {
                    'user_id': str(uuid4()),
                    'new_email': f'{''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(230))}@testmail.com',
                }, not_raises()
            ),
        ]
    )
    async def test_user_email_updated_external_event_handler(
        self, mongodb_db, body, expectation, beanie_notification_repository, message_bus,
    ):
        message_bus.repo = beanie_notification_repository

        handler = UserEmailUpdatedExternalEventHandler(bus=message_bus)
        with expectation:
            await handler(body)

            assert len(beanie_notification_repository.loaded_notifications) == 1
            notification = beanie_notification_repository.loaded_notifications.pop()
            assert len(notification.receivers) == 1
            receiver = notification.receivers[0]

            assert notification.__class__ is EmailNotificationEntity
            assert receiver == EmailVO(body['new_email'])
            assert body['new_email'] in notification.text and body['new_email'] in notification.html


    @pytest.mark.parametrize(
        'body, expectation',
        [
            (
                {
                    'user_id': str(uuid4()),
                    'new_phone_number': f'+{''.join(random.choice(string.digits) for _ in range(14))}',
                }, not_raises()
            ),
        ]
    )
    async def test_user_phone_number_updated_external_event_handler(
        self, mongodb_db, body, expectation, beanie_notification_repository, message_bus,
    ):
        message_bus.repo = beanie_notification_repository

        handler = UserPhoneNumberUpdatedExternalEventHandler(bus=message_bus)
        with expectation:
            await handler(body)

            assert len(beanie_notification_repository.loaded_notifications) == 1
            notification = beanie_notification_repository.loaded_notifications.pop()
            assert len(notification.receivers) == 1
            receiver = notification.receivers[0]

            assert notification.__class__ is SMSNotificationEntity
            assert receiver == PhoneNumberVO(body['new_phone_number'])
            assert body['new_phone_number'] in notification.text
