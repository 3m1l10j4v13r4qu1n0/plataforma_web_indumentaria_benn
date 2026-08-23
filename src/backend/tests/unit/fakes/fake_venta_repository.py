from app.domain.exceptions import TicketDuplicadoError
from app.domain.models.venta import Venta
from app.domain.ports.i_venta_repository import IVentaRepository


class FakeVentaRepository(IVentaRepository):
    def __init__(self):
        self._ventas = []

    async def crear_venta(self, venta: Venta) -> Venta:
        # Espeja el UNIQUE uq_ventas_numero_ticket de la base de datos
        if venta.numero_ticket is not None:
            if any(v.numero_ticket == venta.numero_ticket for v in self._ventas):
                raise TicketDuplicadoError(venta.numero_ticket)

        self._ventas.append(venta)
        return venta

    async def obtener_venta_por_id(self, venta_id: str) -> Venta | None:
        for v in self._ventas:
            if v.id == venta_id:
                return v
        return None

    async def obtener_venta_por_numero_ticket(self, numero_ticket: str) -> Venta | None:
        for v in self._ventas:
            if v.numero_ticket == numero_ticket:
                return v
        return None

    # Método auxiliar para compatibilidad con código existente
    async def obtener_por_id(self, venta_id: str) -> Venta | None:
        return await self.obtener_venta_por_id(venta_id)

    def obtener_ventas(self):
        return self._ventas
