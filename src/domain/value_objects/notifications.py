from dataclasses import dataclass

from domain.exceptions.notifications import (
    EmailIsEmptyException,
    EmailTooShortException,
    EmailTooLongException,
    EmailNotContainingAtSymbolException,
    PhoneNumberIsEmptyException,
    PhoneNumberTooShortException,
    PhoneNumberTooLongException,
    PhoneNumberNotStartingWithPlusSymbolException,
    PhoneNumberContainsNonDigitsException, NameTypeException, NameIsEmptyException, NameTooLongException,
)
from domain.value_objects.base import BaseVO


@dataclass(frozen=True)
class EmailVO(BaseVO):
    value: str

    def validate(self) -> bool:
        if not self.value:
            raise EmailIsEmptyException()

        if len(self.value) < 5:
            raise EmailTooShortException(self.value)

        if len(self.value) > 255:
            raise EmailTooLongException(self.value)

        if '@' not in self.value:
            raise EmailNotContainingAtSymbolException(self.value)

        return True

    def as_generic(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class PhoneNumberVO(BaseVO):
    value: str

    def validate(self) -> bool:
        if not self.value:
            raise PhoneNumberIsEmptyException()

        if len(self.value) < 7:
            raise PhoneNumberTooShortException(self.value)

        if len(self.value) > 15:
            raise PhoneNumberTooLongException(self.value)

        if not self.value.startswith('+'):
            raise PhoneNumberNotStartingWithPlusSymbolException(self.value)

        if not self.value[1:].isdecimal():
            raise PhoneNumberContainsNonDigitsException(self.value)

        return True

    def as_generic(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class NameVO(BaseVO):
    value: str

    def validate(self) -> bool:
        if not isinstance(self.value, str):
            raise NameTypeException

        if not self.value:
            raise NameIsEmptyException

        if len(self.value) > 255:
            raise NameTooLongException(self.value)

        return True

    def as_generic(self) -> str:
        return str(self.value)
