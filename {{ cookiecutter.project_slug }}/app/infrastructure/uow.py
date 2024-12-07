import typing

from scaffold.persistence import GenericSqlUnitOfWork
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.interfaces.uow import UnitOfWork, UnitOfWorkFactory


class SqlUnitOfWork(GenericSqlUnitOfWork, UnitOfWork):
    @typing.override
    def __init__(self, session: AsyncSession) -> None:
        # Add your repositories here...

        super().__init__(session)


class SqlUnitOfWorkFactory(UnitOfWorkFactory):
    def __init__(self, session_factory: typing.Callable[[], AsyncSession]) -> None:
        self._session_factory = session_factory

    @typing.override
    def create(self) -> SqlUnitOfWork:
        return SqlUnitOfWork(self._session_factory())
