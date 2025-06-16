from contextlib import nullcontext as not_raises

import pytest

from domain.exceptions.notifications import (
    PhoneNumberTypeException,
    PhoneNumberIsEmptyException,
    PhoneNumberTooShortException,
    PhoneNumberTooLongException,
    PhoneNumberNotStartingWithPlusSymbolException,
    PhoneNumberContainsNonDigitsException,
)
from domain.value_objects.notifications import PhoneNumberVO


@pytest.mark.parametrize(
    'phone_numbers, expectation',
    [
        (['+12345678910'], not_raises()),
        ([100, 12.3, True, None, [], {}, ()], pytest.raises(PhoneNumberTypeException)),
        ([''], pytest.raises(PhoneNumberIsEmptyException)),
        (['+12345'], pytest.raises(PhoneNumberTooShortException)),
        (['+1234567891001987654321'], pytest.raises(PhoneNumberTooLongException)),
        (['12345678910'], pytest.raises(PhoneNumberNotStartingWithPlusSymbolException)),
        (['+12345678910a', '+*12345678910'], pytest.raises(PhoneNumberContainsNonDigitsException)),
    ]
)
def test_phone_number_vo_inputs(phone_numbers, expectation):
    with expectation:
        for phone_number in phone_numbers:
            PhoneNumberVO(phone_number)


@pytest.mark.parametrize(
    'phone_number1, phone_number2, expectation',
    [
        ('+12345678910', '+12345678910', not_raises()),
        ('+12345678910', '+01987654321', pytest.raises(AssertionError)),
    ]
)
def test_phone_number_vos_equality(phone_number1, phone_number2, expectation):
    with expectation:
        assert PhoneNumberVO(phone_number1) == PhoneNumberVO(phone_number2)
