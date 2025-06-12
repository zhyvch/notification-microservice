from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class ServiceException(Exception):
    @property
    def message(self) -> str:
        return 'Service error occurred'
