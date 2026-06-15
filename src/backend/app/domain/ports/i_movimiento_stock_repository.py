from typing import Protocol

from app.domain.models.movimiento_stock import MovimientoStock


class IMovimientoStockRepository(Protocol):
    async def registrar_movimiento(self, movimiento: MovimientoStock) -> None:
        """
        Registra un movimiento de stock en la base de datos.
        Debe ejecutarse dentro de la misma transacción que la actualización del stock
        para garantizar la atomicidad (ACID).
        """
        ...
