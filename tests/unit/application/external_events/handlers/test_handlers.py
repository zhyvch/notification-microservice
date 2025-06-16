from contextlib import nullcontext as not_raises

import pytest

from application.external_events.handlers.notifications import (
    UserRegistrationCompletedExternalEventHandler,
    UserEmailUpdateInitiatedExternalEventHandler,
    UserPhoneNumberUpdateInitiatedExternalEventHandler,
    UserPasswordResetInitiatedExternalEventHandler,
    UserEmailUpdatedExternalEventHandler,
    UserPhoneNumberUpdatedExternalEventHandler,
)
from domain.entities.notifications import EmailNotificationEntity, SMSNotificationEntity
from domain.exceptions.notifications import (
    InsufficientCredentialsInfoException,
    EmailTypeException,
    EmailIsEmptyException, PhoneNumberIsEmptyException,
)


@pytest.mark.asyncio
class TestExternalEventHandlers:
    @pytest.mark.parametrize(
        'body, expectation',
        [
            (
                {
                    'user_id': '123e4567-e89b-12d3-a456-426614174000',
                    'email': 'example@example.com',
                    'phone_number': '+1234567890',
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'middle_name': 'A',
                    'credentials_status': 'success',
                },
                not_raises()
            ),
            (
                {
                    'user_id': '123e4567-e89b-12d3-a456-426614174000',
                    'email': 'example@example.com',
                    'phone_number': '+1234567890',
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'middle_name': 'A',
                    'credentials_status': 'failed',
                },
                not_raises()
            ),
            (
                {
                    'user_id': '123e4567-e89b-12d3-a456-426614174000',
                    'email': 'example@example.com',
                    'phone_number': '+1234567890',
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'middle_name': 'A',
                    'credentials_status': 'pending',
                },
                not_raises()
            ),
            (
                {
                    'user_id': '123e4567-e89b-12d3-a456-426614174000',
                    'phone_number': '+1234567890',
                    'credentials_status': 'success',
                },
                not_raises()
            ),
            (
                {
                    'user_id': '123e4567-e89b-12d3-a456-426614174000',
                    'email': 'example@example.com',
                    'credentials_status': 'success',
                },
                not_raises()
            ),
            (
                {
                    'user_id': '123e4567-e89b-12d3-a456-426614174000',
                    'credentials_status': 'success',
                },
                pytest.raises(InsufficientCredentialsInfoException)
            ),
        ],
    )
    async def test_user_registration_completed_external_event_handler(
            self, fake_message_bus, body, expectation
    ):
        handler = UserRegistrationCompletedExternalEventHandler(bus=fake_message_bus)
        with expectation:
            await handler(body=body)

            loaded_notifications = [notification for notification in fake_message_bus.repo.loaded_notifications]
            assert len(loaded_notifications) == 1

            if body.get('email'):
                assert loaded_notifications[0].__class__ is EmailNotificationEntity
                assert loaded_notifications[0].receivers[0].as_generic() == body['email']
            else:
                assert loaded_notifications[0].__class__ is SMSNotificationEntity
                assert loaded_notifications[0].receivers[0].as_generic() == body['phone_number']


    @pytest.mark.parametrize(
        'body, expectation',
        [
            (
                {
                    'user_id': '123e4567-e89b-12d3-a456-426614174000',
                    'new_email': 'examle@example.com',
                    'verification_token': 'verification_token_123',
                },
                not_raises()
            ),
            (
                {
                    'user_id': '123e4567-e89b-12d3-a456-426614174000',
                    'new_email': '',
                    'verification_token': 'verification_token_123',
                },
                pytest.raises(EmailIsEmptyException)
            ),
            (
                {
                    'user_id': '123e4567-e89b-12d3-a456-426614174000',
                    'verification_token': 'verification_token_123',
                },
                pytest.raises(KeyError)
            ),
        ],
    )
    async def test_user_email_update_initiated_external_event_handler(
            self, fake_message_bus, body, expectation
    ):
        handler = UserEmailUpdateInitiatedExternalEventHandler(bus=fake_message_bus)
        with expectation:
            await handler(body=body)

            loaded_notifications = [notification for notification in fake_message_bus.repo.loaded_notifications]
            assert len(loaded_notifications) == 1
            assert loaded_notifications[0].__class__ is EmailNotificationEntity
            assert loaded_notifications[0].receivers[0].as_generic() == body['new_email']


    @pytest.mark.parametrize(
        'body, expectation',
        [
            (
                {
                    'user_id': '123e4567-e89b-12d3-a456-426614174000',
                    'new_phone_number': '+1234567890',
                    'verification_token': 'verification_token_123',
                },
                not_raises()
            ),
            (
                {
                    'user_id': '123e4567-e89b-12d3-a456-426614174000',
                    'new_phone_number': '',
                    'verification_token': 'verification_token_123',
                },
                pytest.raises(PhoneNumberIsEmptyException)
            ),
            (
                {
                    'user_id': '123e4567-e89b-12d3-a456-426614174000',
                    'verification_token': 'verification_token_123',
                },
                pytest.raises(KeyError)
            ),
        ],
    )
    async def test_user_phone_number_update_initiated_external_event_handler(
            self, fake_message_bus, body, expectation
    ):
        handler = UserPhoneNumberUpdateInitiatedExternalEventHandler(bus=fake_message_bus)
        with expectation:
            await handler(body=body)

            loaded_notifications = [notification for notification in fake_message_bus.repo.loaded_notifications]
            assert len(loaded_notifications) == 1
            assert loaded_notifications[0].__class__ is SMSNotificationEntity
            assert loaded_notifications[0].receivers[0].as_generic() == body['new_phone_number']


    @pytest.mark.parametrize(
        'body, expectation',
        [
            (
                {
                    'user_id': '123e4567-e89b-12d3-a456-426614174000',
                    'email': 'example@example.com',
                    'verification_token': 'verification_token_123',
                },
                not_raises()
            ),
            (
                {
                    'user_id': '123e4567-e89b-12d3-a456-426614174000',
                    'phone_number': '+1234567890',
                    'verification_token': 'verification_token_123',
                },
                not_raises()
            ),
            (
                {
                    'user_id': '123e4567-e89b-12d3-a456-426614174000',
                    'verification_token': 'verification_token_123',
                },
                pytest.raises(InsufficientCredentialsInfoException)
            ),
            (
                {
                    'user_id': '123e4567-e89b-12d3-a456-426614174000',
                },
                pytest.raises(KeyError)
            ),
        ],
    )
    async def test_user_password_reset_initiated_external_event_handler(
            self, fake_message_bus, body, expectation
    ):
        handler = UserPasswordResetInitiatedExternalEventHandler(bus=fake_message_bus)
        with expectation:
            await handler(body=body)

            loaded_notifications = [notification for notification in fake_message_bus.repo.loaded_notifications]
            assert len(loaded_notifications) == 1

            if body.get('email'):
                assert loaded_notifications[0].__class__ is EmailNotificationEntity
                assert loaded_notifications[0].receivers[0].as_generic() == body['email']
            else:
                assert loaded_notifications[0].__class__ is SMSNotificationEntity
                assert loaded_notifications[0].receivers[0].as_generic() == body['phone_number']


    @pytest.mark.parametrize(
        'body, expectation',
        [
            (
                {
                    'user_id': '123e4567-e89b-12d3-a456-426614174000',
                    'new_email': 'example@example.com',
                },
                not_raises()
            ),
            (
                {
                    'user_id': '123e4567-e89b-12d3-a456-426614174000',
                    'new_email': '',
                },
                pytest.raises(EmailIsEmptyException)
            ),
            (
                {
                    'user_id': '123e4567-e89b-12d3-a456-426614174000',
                },
                pytest.raises(KeyError)
            ),
        ],
    )
    async def test_user_email_updated_external_event_handler(
            self, fake_message_bus, body, expectation
    ):
        handler = UserEmailUpdatedExternalEventHandler(bus=fake_message_bus)
        with expectation:
            await handler(body=body)

            loaded_notifications = [notification for notification in fake_message_bus.repo.loaded_notifications]
            assert len(loaded_notifications) == 1
            assert loaded_notifications[0].__class__ is EmailNotificationEntity
            assert loaded_notifications[0].receivers[0].as_generic() == body['new_email']


    @pytest.mark.parametrize(
        'body, expectation',
        [
            (
                {
                    'user_id': '123e4567-e89b-12d3-a456-426614174000',
                    'new_phone_number': '+1234567890',
                },
                not_raises()
            ),
            (
                {
                    'user_id': '123e4567-e89b-12d3-a456-426614174000',
                    'new_phone_number': '',
                },
                pytest.raises(PhoneNumberIsEmptyException)
            ),
            (
                {
                    'user_id': '123e4567-e89b-12d3-a456-426614174000',
                },
                pytest.raises(KeyError)
            ),
        ],
    )
    async def test_user_phone_number_updated_external_event_handler(
            self, fake_message_bus, body, expectation
    ):
        handler = UserPhoneNumberUpdatedExternalEventHandler(bus=fake_message_bus)
        with expectation:
            await handler(body=body)

            loaded_notifications = [notification for notification in fake_message_bus.repo.loaded_notifications]
            assert len(loaded_notifications) == 1
            assert loaded_notifications[0].__class__ is SMSNotificationEntity
            assert loaded_notifications[0].receivers[0].as_generic() == body['new_phone_number']
