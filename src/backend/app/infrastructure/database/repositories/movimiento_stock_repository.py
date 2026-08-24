"""Implementación del puerto IMovimientoStockRepository sobre SQLAlchemy."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.exceptions import StockUpdateException
from app.domain.models.movimiento_stock import MovimientoStock
from app.domain.ports.i_movimiento_stock_repository import IMovimientoStockRepository
from app.infrastructure.database.orm_models.movimiento_stock_orm import (
    MovimientoStockORM,
)


class MovimientoStockRepository(IMovimientoStockRepository):
    """Persiste movimientos de stock dentro de la transacción vigente.

    No hace commit: la confirmación la controla el Unit of Work para que la
    actualización del stock y su registro de auditoría sean atómicos (HU-08).
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def registrar(self, movimiento: MovimientoStock) -> MovimientoStock:
        """Inserta el movimiento y sincroniza con la BD sin confirmar.

        Args:
            movimiento: Entidad de dominio a persistir.

        Returns:
            La entidad de dominio registrada.

        Raises:
            StockUpdateException: Si la BD rechaza el insert (violación de
                constraints u otro error de integridad).
        """
        orm_movimiento = MovimientoStockORM(
            id=movimiento.id,
            producto_id=movimiento.producto_id,
            tipo_movimiento=movimiento.tipo_movimiento.value,
            cantidad=movimiento.cantidad,
            fecha_hora=movimiento.fecha_hora,
            documento_referencia_id=movimiento.documento_referencia_id,
        )

        self.session.add(orm_movimiento)

        try:
            # flush envía el INSERT y dispara los constraints sin cerrar la transacción.
            await self.session.flush()
        except Exception as exc:
            await self.session.rollback()
            raise StockUpdateException(
                producto_id=movimiento.producto_id,
                motivo=(
                    f"no se pudo registrar el movimiento de stock ({exc.orig})"
                    if hasattr(exc, "orig")
                    else f"no se pudo registrar el movimiento de stock ({exc})"
                ),
            ) from exc

        return movimiento
