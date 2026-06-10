from app.domain.models.venta import Venta
from app.domain.ports.i_venta_repository import IVentaRepository


class FakeVentaRepository(IVentaRepository):
    def __init__(self):
        self._ventas = []

    async def crear_venta(self, venta: Venta) -> Venta:
        self._ventas.append(venta)
        return venta

    def obtener_ventas(self):
        return self._ventas
