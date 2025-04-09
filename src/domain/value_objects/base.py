from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Any

from typing_extensions import Generic

VT = TypeVar('VT', bound=Any)


@dataclass(frozen=True)
class BaseVO(ABC, Generic[VT]):
    value: VT

    def __post_init__(self):
        self.validate()

    @abstractmethod
    def validate(self) -> bool:
        pass

    @abstractmethod
    def as_generic(self) -> VT:
        pass
