from uuid import UUID
from contextlib import nullcontext as not_raises

from domain.entities.notifications import EmailNotificationEntity, SMSNotificationEntity

import pytest

from domain.value_objects.notifications import EmailVO, PhoneNumberVO
from tests.config import test_settings


@pytest.mark.parametrize(
    'email_notification1, email_notification2, expectation',
    [
        (EmailNotificationEntity(
            id=UUID('0e6315a5-7980-4a14-a902-29a428054c8a'),
            sender=EmailVO(test_settings.TESTS_FROM_EMAIL),
            receivers=[EmailVO('example@email.com')],
            subject='Test Subject',
            text='Test Text',
            html='<p>Test HTML</p>',
        ), EmailNotificationEntity(
            id=UUID('0e6315a5-7980-4a14-a902-29a428054c8a'),
            sender=EmailVO(test_settings.TESTS_FROM_EMAIL),
            receivers=[EmailVO('example@email.com')],
            subject='Test Subject',
            text='Test Text',
            html='<p>Test HTML</p>',
        ), not_raises()),
        (EmailNotificationEntity(
            id=UUID('0e6315a5-7980-4a14-a902-29a428054c8a'),
            sender=EmailVO(test_settings.TESTS_FROM_EMAIL),
            receivers=[EmailVO('example@email.com')],
            subject='Test Subject',
            text='Test Text',
            html='<p>Test HTML</p>',
        ), EmailNotificationEntity(
            id=UUID('0e6315a5-7980-0000-a902-29a428054c8a'),
            sender=EmailVO(test_settings.TESTS_FROM_EMAIL),
            receivers=[EmailVO('example@email.com')],
            subject='Test Subject',
            text='Test Text',
            html='<p>Test HTML</p>',
        ), pytest.raises(AssertionError)),
    ]
)
def test_email_notification_entity(email_notification1, email_notification2, expectation):
    with expectation:
        assert email_notification1 == email_notification2


@pytest.mark.parametrize(
    'sms_notification1, sms_notification2, expectation',
    [
        (SMSNotificationEntity(
            id=UUID('0e6315a5-7980-4a14-a902-29a428054c8a'),
            sender=PhoneNumberVO(test_settings.TESTS_FROM_PHONE_NUMBER),
            receivers=[PhoneNumberVO('+12345678910')],
            text='Test SMS Text'
        ), SMSNotificationEntity(
            id=UUID('0e6315a5-7980-4a14-a902-29a428054c8a'),
            sender=PhoneNumberVO(test_settings.TESTS_FROM_PHONE_NUMBER),
            receivers=[PhoneNumberVO('+12345678910')],
            text='Test SMS Text'
        ), not_raises()),
        (SMSNotificationEntity(
            id=UUID('0e6315a5-7980-4a14-a902-29a428054c8a'),
            sender=PhoneNumberVO(test_settings.TESTS_FROM_PHONE_NUMBER),
            receivers=[PhoneNumberVO('+12345678910')],
            text='Test SMS Text'
        ), SMSNotificationEntity(
            id=UUID('0e6315a5-7980-0000-a902-29a428054c8a'),
            sender=PhoneNumberVO(test_settings.TESTS_FROM_PHONE_NUMBER),
            receivers=[PhoneNumberVO('+12345678910')],
            text='Test SMS Text'
        ), pytest.raises(AssertionError)),
    ]
)
def test_sms_notification_entity(sms_notification1, sms_notification2, expectation):
    with expectation:
        assert sms_notification1 == sms_notification2





