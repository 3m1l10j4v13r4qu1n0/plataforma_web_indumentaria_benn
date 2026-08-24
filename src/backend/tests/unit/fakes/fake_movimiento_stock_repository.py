from app.domain.models.movimiento_stock import MovimientoStock
from app.domain.ports.i_movimiento_stock_repository import IMovimientoStockRepository


class FakeMovimientoStockRepository(IMovimientoStockRepository):
    """Fake en memoria del repositorio de movimientos de stock."""

    def __init__(self):
        self._movimientos: list[MovimientoStock] = []

    def agregar_movimientos(self, movimientos: list[MovimientoStock]) -> None:
        self._movimientos.extend(movimientos)

    async def registrar(self, movimiento: MovimientoStock) -> MovimientoStock:
        self._movimientos.append(movimiento)
        return movimiento

    def obtener_por_producto(self, producto_id: str) -> list[MovimientoStock]:
        return [m for m in self._movimientos if m.producto_id == producto_id]

    def obtener_todos(self) -> list[MovimientoStock]:
        return list(self._movimientos)

    def limpiar(self) -> None:
        self._movimientos.clear()
