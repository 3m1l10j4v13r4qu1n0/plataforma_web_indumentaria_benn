"""Implementación del patrón Unit of Work sobre una sesión asíncrona compartida."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.ports.i_unit_of_work import IUnitOfWork


class UnitOfWorkSQLAlchemy(IUnitOfWork):
    """Delimita la transacción de la sesión compartida entre repositorios.

    Los repositorios concretos comparten la misma `AsyncSession`; este
    componente es el único autorizado a confirmar o revertir la transacción
    cuando un caso de uso necesita atomicidad entre varios agregados.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self) -> None:
        """Confirma todos los cambios pendientes de la transacción actual."""
        await self.session.commit()

    async def rollback(self) -> None:
        """Revierte todos los cambios pendientes de la transacción actual."""
        await self.session.rollback()
