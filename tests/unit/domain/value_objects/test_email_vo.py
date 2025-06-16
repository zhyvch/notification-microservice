from contextlib import nullcontext as not_raises

import pytest

from domain.exceptions.notifications import (
    EmailTypeException,
    EmailIsEmptyException,
    EmailTooShortException,
    EmailTooLongException,
    EmailNotContainingAtSymbolException,
)
from domain.value_objects.notifications import EmailVO


@pytest.mark.parametrize(
    'emails, expectation',
    [
        (['successful@emaple.com'], not_raises()),
        ([100, 12.3, True, None, [], {}, ()], pytest.raises(EmailTypeException)),
        ([''], pytest.raises(EmailIsEmptyException)),
        (['a@b.c'], pytest.raises(EmailTooShortException)),
        ([f'a' * 250 + 'example.com'], pytest.raises(EmailTooLongException)),
        (['failed.emaple.com'], pytest.raises(EmailNotContainingAtSymbolException)),
    ]
)
def test_email_vo_inputs(emails, expectation):
    with expectation:
        for email in emails:
            EmailVO(email)


@pytest.mark.parametrize(
    'email1, email2, expectation',
    [
        ('same@email.com', 'same@email.com', not_raises()),
        ('same@email.com', 'different@email.com', pytest.raises(AssertionError)),
    ]
)
def test_email_vos_equality(email1, email2, expectation):
    with expectation:
        assert EmailVO(email1) == EmailVO(email2)
