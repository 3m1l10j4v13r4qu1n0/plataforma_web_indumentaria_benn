# app/domain/ports/i_venta_repository.py
from typing import Protocol

from app.domain.models.venta import Venta


class IVentaRepository(Protocol):
    def crear_venta(self, venta: Venta) -> Venta: ...
