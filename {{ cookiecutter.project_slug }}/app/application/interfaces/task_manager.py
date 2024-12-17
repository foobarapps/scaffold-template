import abc
import typing


class TaskManager(abc.ABC):
    @abc.abstractmethod
    def run_task(
        self,
        func: typing.Callable,
        *args: typing.Any,  # noqa: ANN401
        **kwargs: typing.Any,  # noqa: ANN401
    ) -> None:
        pass
