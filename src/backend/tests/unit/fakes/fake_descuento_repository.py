from typing import Dict, Optional

from app.domain.models.descuento import Descuento
from app.domain.ports.i_descuento_repository import IDescuentoRepository


class FakeDescuentoRepository(IDescuentoRepository):
    """Implementación en memoria del repositorio de descuentos para pruebas."""

    def __init__(self):
        self._descuentos: Dict[str, Descuento] = {}

    def agregar_descuento(self, descuento: Descuento):
        self._descuentos[descuento.id] = descuento

    async def crear_descuento(self, descuento: Descuento) -> Descuento:
        self._descuentos[descuento.id] = descuento
        return descuento

    async def obtener_por_venta_id(self, venta_id: str) -> Optional[Descuento]:
        for d in self._descuentos.values():
            if d.venta_id == venta_id:
                return d
        return None

    async def obtener_por_id(self, descuento_id: str) -> Optional[Descuento]:
        return self._descuentos.get(descuento_id)

    def obtener_todos(self) -> list[Descuento]:
        return list(self._descuentos.values())
