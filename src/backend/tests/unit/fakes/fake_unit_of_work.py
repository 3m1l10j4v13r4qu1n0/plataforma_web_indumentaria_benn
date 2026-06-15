from app.domain.ports.i_unit_of_work import IUnitOfWork


class FakeUnitOfWork(IUnitOfWork):
    def __init__(self):
        self.commit_called = False
        self.rollback_called = False

    async def commit(self) -> None:
        self.commit_called = True

    async def rollback(self) -> None:
        self.rollback_called = True
