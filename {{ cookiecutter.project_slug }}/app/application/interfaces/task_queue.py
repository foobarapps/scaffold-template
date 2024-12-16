import abc
import dataclasses
from collections.abc import Callable
from typing import Protocol


@dataclasses.dataclass(frozen=True)
class Task:
    pass


class TaskHandler(abc.ABC):
    @abc.abstractmethod
    async def handle_task(self, task: Task) -> None:
        pass


class TaskQueue(Protocol):
    async def init(self) -> None: ...

    async def enqueue(self, task: Task) -> None: ...

    def register(
        self,
        task_type: type[Task],
        handler_factory: Callable[[], TaskHandler],
    ) -> None: ...

    async def handle_tasks(self) -> None: ...
