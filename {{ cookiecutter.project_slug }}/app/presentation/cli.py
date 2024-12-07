from scaffold.cli import BaseCLIApp, command

from app.application.interfaces import TaskQueue


class CLIApp(BaseCLIApp):
    def __init__(
        self,
        task_queue: TaskQueue,
    ) -> None:
        super().__init__()
        self.task_queue = task_queue

    @command("task-queue-worker")
    async def task_queue_worker(self) -> None:
        await self.task_queue.init()
        await self.task_queue.handle_tasks()
