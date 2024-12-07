import os

from psycopg_pool import AsyncConnectionPool
from scaffold.di import Container
from scaffold.mail_sender import SmtpMailSender
from scaffold.pub_sub import PostgresPubSubService
from scaffold.task_queue import PostgresTaskQueue
from scaffold.utils import find_subclasses, get_env_flag, get_postgresql_url
from scaffold.web.base_controller import BaseController
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.application.backgroundtasks import handlers as handlers_pkg
from app.application.backgroundtasks.handlers.base import BaseTaskHandler
from app.application.interfaces import (
    NotificationService,
    PubSubService,
    TaskQueue,
)
from app.application.interfaces.task_queue import Task, TaskHandler
from app.application.interfaces.uow import UnitOfWorkFactory
from app.infrastructure.services.emailnotificationservice import (
    EmailNotificationService,
)
from app.infrastructure.uow import SqlUnitOfWorkFactory
from app.presentation.web import WebApp
from app.presentation.web import controllers as controllers_pkg


def web_app_factory(container: Container) -> WebApp:
    app = WebApp(
        "app.presentation.web",
        secret_key=bytes.fromhex(os.environ["SECRET_KEY"]),
        server_name=os.environ["DOMAIN"],
        propagate_exceptions=get_env_flag("PROPAGATE_EXCEPTIONS"),
    )

    controller_classes = find_subclasses(controllers_pkg, BaseController)

    controller_factories = {cls: container.get_factory(cls) for cls in controller_classes}
    app.register_controllers(controller_factories)

    return app


def task_queue_factory(container: Container) -> TaskQueue:
    task_queue: TaskQueue = PostgresTaskQueue[Task, TaskHandler](connection_pool=container[AsyncConnectionPool])

    task_handler_classes = find_subclasses(handlers_pkg, BaseTaskHandler)

    for task_handler_class in task_handler_classes:
        task_class: type[Task] = task_handler_class.get_task_type()
        task_queue.register(task_class, container.get_factory(task_handler_class))

    return task_queue


def bootstrap() -> Container:
    container = Container()

    engine = create_async_engine(get_postgresql_url(for_sqlalchemy=True))
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    container.add_singleton(AsyncConnectionPool, lambda _: AsyncConnectionPool(get_postgresql_url(), open=False))
    container.add_singleton(UnitOfWorkFactory, lambda _: SqlUnitOfWorkFactory(session_factory))
    container.add_singleton(PubSubService, lambda c: PostgresPubSubService(connection_pool=c[AsyncConnectionPool]))
    container.add_singleton(TaskQueue, task_queue_factory)

    async def init_services(c: Container) -> None:
        await c[TaskQueue].init()
        await c[PubSubService].init()

    container.add_init_function(init_services)

    container.add_singleton(WebApp, web_app_factory)

    if os.getenv("MAIL_HOSTNAME"):

        def email_notification_service_factory(container: Container) -> EmailNotificationService:
            mail_sender = SmtpMailSender(
                host=os.environ["MAIL_HOSTNAME"],
                port=int(os.environ["MAIL_PORT"]),
                username=os.getenv("MAIL_USERNAME"),
                password=os.getenv("MAIL_PASSWORD"),
            )
            email_notification_service = EmailNotificationService(
                web_app=container[WebApp],
                mail_sender=mail_sender,
                default_sender_email=os.environ["MAIL_DEFAULT_SENDER"],
            )
            return email_notification_service

        container.add_transient(NotificationService, email_notification_service_factory)

    return container
