import abc
import dataclasses
import uuid
from typing import override


@dataclasses.dataclass(frozen=True)
class EntityId:
    value: uuid.UUID


class Entity(abc.ABC):
    @property
    @abc.abstractmethod
    def id(self) -> EntityId: ...

    @override
    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.id == other.id

    @override
    def __hash__(self) -> int:
        return hash(self.id)


class Repository:
    pass
