from app.domain.ports.i_unit_of_work import IUnitOfWork


class FakeUnitOfWork(IUnitOfWork):
    """Fake en memoria del Unit of Work: cuenta commits y rollbacks."""

    def __init__(self):
        self.commits: int = 0
        self.rollbacks: int = 0

    async def commit(self) -> None:
        self.commits += 1

    async def rollback(self) -> None:
        self.rollbacks += 1
