# app/domain/ports/i_venta_repository.py
from typing import Protocol

from app.domain.models.venta import EstadoVenta, Venta


class IVentaRepository(Protocol):
    async def crear_venta(self, venta: Venta) -> Venta: ...

    async def obtener_venta_por_id(self, venta_id: str) -> Venta | None: ...

    async def obtener_venta_por_numero_ticket(
        self, numero_ticket: str
    ) -> Venta | None: ...

    async def actualizar_estado(
        self, numero_ticket: str, nuevo_estado: EstadoVenta
    ) -> Venta | None: ...
