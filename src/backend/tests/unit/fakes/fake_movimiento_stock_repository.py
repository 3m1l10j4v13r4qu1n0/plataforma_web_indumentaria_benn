from typing import List
from app.domain.models.movimiento_stock import MovimientoStock
from app.domain.ports.i_movimiento_stock_repository import IMovimientoStockRepository

class FakeMovimientoStockRepository(IMovimientoStockRepository):
    def __init__(self):
        self.movimientos: List[MovimientoStock] = []

    async def registrar_movimiento(self, movimiento: MovimientoStock) -> None:
        self.movimientos.append(movimiento)