from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(frozen=True, eq=False)
class EmailIsEmptyException(ApplicationException):
    @property
    def message(self) -> str:
        return 'Email is empty'


@dataclass(frozen=True, eq=False)
class EmailTooShortException(ApplicationException):
    email: str

    @property
    def message(self) -> str:
        return f'Email <{self.email}> is too short'


@dataclass(frozen=True, eq=False)
class EmailTooLongException(ApplicationException):
    email: str

    @property
    def message(self) -> str:
        return f'Email <{self.email[255:]}...> is too long'


@dataclass(frozen=True, eq=False)
class EmailNotContainingAtSymbolException(ApplicationException):
    email: str

    @property
    def message(self) -> str:
        return f'Email <{self.email}> must contain an "@" symbol'


@dataclass(frozen=True, eq=False)
class PhoneNumberIsEmptyException(ApplicationException):
    @property
    def message(self) -> str:
        return 'Phone number is empty'


@dataclass(frozen=True, eq=False)
class PhoneNumberTooShortException(ApplicationException):
    phone_number: str

    @property
    def message(self) -> str:
        return f'Phone number <{self.phone_number[15:]}...> is too short'


@dataclass(frozen=True, eq=False)
class PhoneNumberTooLongException(ApplicationException):
    phone_number: str

    @property
    def message(self) -> str:
        return f'Phone number <{self.phone_number[15:]}...> is too long'


@dataclass(frozen=True, eq=False)
class PhoneNumberNotStartingWithPlusSymbolException(ApplicationException):
    phone_number: str

    @property
    def message(self) -> str:
        return f'Phone number <{self.phone_number}> must start with "+" symbol'


@dataclass(frozen=True, eq=False)
class PhoneNumberContainsNonDigitsException(ApplicationException):
    phone_number: str

    @property
    def message(self) -> str:
        return f'Phone number <{self.phone_number}> must contain only digits'