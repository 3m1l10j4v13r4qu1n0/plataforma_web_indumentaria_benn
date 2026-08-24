"""Puerto que delimita la transacción atómica compartida entre repositorios."""

from typing import Protocol


class IUnitOfWork(Protocol):
    """Contrato de control transaccional (patrón Unit of Work).

    Permite que un caso de uso agruple varias operaciones de distintos
    repositorios (que comparten la misma sesión) en una única transacción
    ACID, decidiendo explícitamente cuándo confirmar o revertir.
    """

    async def commit(self) -> None:
        """Confirma todos los cambios pendientes de la transacción actual."""
        ...

    async def rollback(self) -> None:
        """Revierte todos los cambios pendientes de la transacción actual."""
        ...
