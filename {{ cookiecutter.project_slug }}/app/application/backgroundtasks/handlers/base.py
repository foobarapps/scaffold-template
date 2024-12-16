import abc
from types import get_original_bases
from typing import final, get_args, override

from app.application.interfaces.task_queue import Task, TaskHandler


class GenericBaseTaskHandler[T](TaskHandler):
    @abc.abstractmethod
    async def handle(self, task: T) -> None:
        pass

    @final
    @override
    async def handle_task(self, task: Task) -> None:
        assert isinstance(task, self.get_task_type())
        # TODO check if coroutine?
        return await self.handle(task)

    @classmethod
    def get_task_type(cls) -> type[T]:
        return get_args(get_original_bases(cls)[0])[0]
