from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class DomainException(Exception):
    @property
    def message(self) -> str:
        return 'Domain error occurred'
