from contextlib import nullcontext as not_raises

import pytest

from domain.exceptions.notifications import (
    NameTypeException,
    NameIsEmptyException,
    NameTooLongException,
)
from domain.value_objects.notifications import NameVO


@pytest.mark.parametrize(
    'names, expectation',
    [
        (['John', 'Jane', 'Doe'], not_raises()),
        ([100, 12.3, True, None, [], {}, ()], pytest.raises(NameTypeException)),
        ([''], pytest.raises(NameIsEmptyException)),
        (['A' * 256], pytest.raises(NameTooLongException)),
    ]
)
def test_name_vo_inputs(names, expectation):
    with expectation:
        for name in names:
            NameVO(name)


@pytest.mark.parametrize(
    'name1, name2, expectation',
    [
        ('Jane', 'Jane', not_raises()),
        ('Jane', 'Doe', pytest.raises(AssertionError)),
    ]
)
def test_name_vos_equality(name1, name2, expectation):
    with expectation:
        assert NameVO(name1) == NameVO(name2)
