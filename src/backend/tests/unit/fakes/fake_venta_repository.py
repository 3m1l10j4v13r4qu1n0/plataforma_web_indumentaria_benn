"""
Ampliamos el fake para almacenar y recuperar ventas por su numero_ticket,
simulando fielmente el comportamiento del repositorio real.

"""

from typing import Dict, Optional

from app.domain.models.venta import Venta
from app.domain.ports.i_venta_repository import IVentaRepository


class FakeVentaRepository(IVentaRepository):
    def __init__(self):
        self._ventas_por_id: Dict[str, Venta] = {}
        self._ventas_por_ticket: Dict[str, Venta] = {}

    def agregar_venta(self, venta: Venta):
        self._ventas_por_id[venta.id] = venta
        self._ventas_por_ticket[venta.numero_ticket] = venta

    async def crear_venta(self, venta: Venta) -> Venta:
        self.agregar_venta(venta)
        return venta

    async def obtener_por_numero_ticket(self, numero_ticket: str) -> Optional[Venta]:
        return self._ventas_por_ticket.get(numero_ticket)
