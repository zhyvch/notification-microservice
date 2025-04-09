from abc import ABC
from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class BaseCommand(ABC):
    command_id: UUID = field(default_factory=uuid4, kw_only=True)
