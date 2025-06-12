from dataclasses import dataclass

from domain.exceptions.base import DomainException


@dataclass(frozen=True, eq=False)
class EmailIsEmptyException(DomainException):
    @property
    def message(self) -> str:
        return 'Email is empty'


@dataclass(frozen=True, eq=False)
class EmailTooShortException(DomainException):
    email: str

    @property
    def message(self) -> str:
        return f'Email <{self.email}> is too short'


@dataclass(frozen=True, eq=False)
class EmailTooLongException(DomainException):
    email: str

    @property
    def message(self) -> str:
        return f'Email <{self.email[255:]}...> is too long'


@dataclass(frozen=True, eq=False)
class EmailNotContainingAtSymbolException(DomainException):
    email: str

    @property
    def message(self) -> str:
        return f'Email <{self.email}> must contain an "@" symbol'


@dataclass(frozen=True, eq=False)
class PhoneNumberIsEmptyException(DomainException):
    @property
    def message(self) -> str:
        return 'Phone number is empty'


@dataclass(frozen=True, eq=False)
class PhoneNumberTooShortException(DomainException):
    phone_number: str

    @property
    def message(self) -> str:
        return f'Phone number <{self.phone_number[15:]}...> is too short'


@dataclass(frozen=True, eq=False)
class PhoneNumberTooLongException(DomainException):
    phone_number: str

    @property
    def message(self) -> str:
        return f'Phone number <{self.phone_number[15:]}...> is too long'


@dataclass(frozen=True, eq=False)
class PhoneNumberNotStartingWithPlusSymbolException(DomainException):
    phone_number: str

    @property
    def message(self) -> str:
        return f'Phone number <{self.phone_number}> must start with "+" symbol'


@dataclass(frozen=True, eq=False)
class PhoneNumberContainsNonDigitsException(DomainException):
    phone_number: str

    @property
    def message(self) -> str:
        return f'Phone number <{self.phone_number}> must contain only digits'


@dataclass(frozen=True, eq=False)
class NameTypeException(DomainException):
    @property
    def message(self) -> str:
        return 'Name should be a string type'


@dataclass(frozen=True, eq=False)
class NameIsEmptyException(DomainException):
    @property
    def message(self) -> str:
        return 'Name is empty'


@dataclass(frozen=True, eq=False)
class NameTooLongException(DomainException):
    name: str

    @property
    def message(self) -> str:
        return f'Name <{self.name[255:]}...> is too long'


@dataclass(frozen=True, eq=False)
class InsufficientCredentialsInfoException(DomainException):
    @property
    def message(self) -> str:
        return 'All credentials are empty. Either email or phone number must be provided.'
