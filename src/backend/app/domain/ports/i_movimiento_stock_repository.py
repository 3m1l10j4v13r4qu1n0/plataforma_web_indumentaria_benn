"""Puerto para la persistencia de movimientos de stock (auditoría)."""

from typing import Protocol

from app.domain.models.movimiento_stock import MovimientoStock


class IMovimientoStockRepository(Protocol):
    """Contrato de persistencia para el historial de movimientos de stock.

    Las implementaciones deben insertar el registro dentro de la transacción
    vigente de la sesión compartida, sin hacer commit, para que la
    actualización de stock y su movimiento de auditoría sean atómicos (HU-08).
    """

    async def registrar(self, movimiento: MovimientoStock) -> MovimientoStock:
        """Registra un movimiento de stock en la unidad de trabajo actual.

        Args:
            movimiento: Movimiento a persistir.

        Returns:
            El movimiento registrado con sus datos definitivos.
        """
        ...
