# Standard Library
from enum import Enum
from typing import Tuple


class BaseEnum(Enum):
    @classmethod
    def list(cls) -> Tuple[str, ...]:  # noqa  # pragma: no cover
        return tuple(item.value for item in cls)


class StrEnum(str, BaseEnum):
    ...
