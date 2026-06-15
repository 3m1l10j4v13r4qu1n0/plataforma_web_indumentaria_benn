from typing import Protocol


class IUnitOfWork(Protocol):
    async def commit(self) -> None:
        """Confirma todos los cambios pendientes en la transacción actual."""
        ...

    async def rollback(self) -> None:
        """Revierte todos los cambios pendientes en la transacción actual."""
        ...
