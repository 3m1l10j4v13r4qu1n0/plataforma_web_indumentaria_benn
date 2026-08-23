# app/domain/ports/i_cambio_repository.py
from typing import Protocol

from app.domain.models.cambio import Cambio


class ICambioRepository(Protocol):
    async def crear_cambio(self, cambio: Cambio) -> Cambio: ...

    async def obtener_cambio_por_id(self, cambio_id: str) -> Cambio | None: ...

    async def obtener_cambios_por_venta(self, venta_id: str) -> list[Cambio]: ...

    async def actualizar_cambio(self, cambio: Cambio) -> Cambio: ...
