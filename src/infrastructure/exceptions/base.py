from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class InfrastructureException(Exception):
    @property
    def message(self) -> str:
        return 'Infrastructure error occurred'
