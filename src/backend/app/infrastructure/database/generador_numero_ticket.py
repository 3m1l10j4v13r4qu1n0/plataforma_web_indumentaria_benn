from collections.abc import Callable
from datetime import UTC, datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.orm_models.venta_orm import VentaORM


def _utc_now() -> datetime:
    """Devuelve el instante actual en UTC."""
    return datetime.now(UTC)


class GeneradorNumeroTicket:
    """Adaptador que genera números de ticket únicos y secuenciales por día.

    Implementa el puerto IGeneradorNumeroTicket con el formato T-YYYYMMDD-NNN,
    consultando el último ticket emitido en la fecha actual (UTC).
    """

    def __init__(self, session: AsyncSession, reloj: Callable[[], datetime] = _utc_now):
        self._session = session
        self._reloj = reloj

    async def generar(self) -> str:
        """Genera el próximo número de ticket para la fecha actual.

        Returns:
            El número de ticket con formato T-YYYYMMDD-NNN.
        """
        fecha = self._reloj().strftime("%Y%m%d")
        prefijo = f"T-{fecha}-"

        stmt = select(func.max(VentaORM.numero_ticket)).where(
            VentaORM.numero_ticket.like(f"{prefijo}%")
        )
        result = await self._session.execute(stmt)
        ultimo = result.scalar_one_or_none()

        if ultimo is None:
            secuencia = 1
        else:
            secuencia = int(ultimo.removeprefix(prefijo)) + 1

        return f"{prefijo}{secuencia:03d}"
