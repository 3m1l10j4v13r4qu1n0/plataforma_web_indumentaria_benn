from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.ports.i_unit_of_work import IUnitOfWork


class UnitOfWork(IUnitOfWork):
    """
    Implementación concreta del patrón Unit of Work para SQLAlchemy Async.

    Responsabilidad Única (SRP):
    - Gestionar los límites de la transacción de base de datos.
    - Garantizar atomicidad (ACID) entre múltiples operaciones de repositorios
      que comparten la misma AsyncSession.

    NOTA IMPORTANTE:
    - Esta clase NO crea ni cierra la sesión. La gestión del ciclo de vida
      (apertura y cierre) se delega a `get_async_session()` en session.py.
    - El Unit of Work solo se encarga de confirmar (commit) o revertir (rollback)
      los cambios dentro de la transacción activa.
    - Todos los repositorios inyectados en un mismo Caso de Uso reciben la
      MISMA instancia de AsyncSession, por lo que comparten la transacción.
    """

    def __init__(self, session: AsyncSession):
        """
        Inyecta la sesión asíncrona compartida con los repositorios.
        Esta sesión proviene de la dependencia Transient `get_async_session()`.
        """
        self._session = session

    @property
    def session(self) -> AsyncSession:
        """Exponer la sesión para casos donde el repositorio necesite acceso directo."""
        return self._session

    async def commit(self) -> None:
        """
        Confirma todos los cambios pendientes en la transacción actual.

        Si algún repositorio falló antes (ej: violación de constraint,
        excepción de dominio), este commit nunca se ejecutará porque
        el Caso de Uso habrá lanzado la excepción antes de llegar aquí.
        """
        await self._session.commit()

    async def rollback(self) -> None:
        """
        Revierte todos los cambios pendientes en la transacción actual.

        Se invoca desde el bloque `except` del Caso de Uso cuando ocurre
        cualquier error (infraestructura o dominio), garantizando que
        ninguna operación parcial quede persistida.
        """
        await self._session.rollback()
