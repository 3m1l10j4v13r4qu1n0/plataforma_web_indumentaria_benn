from app.domain.exceptions import CambioNoEncontradoError
from app.domain.models.cambio import Cambio
from app.domain.ports.i_cambio_repository import ICambioRepository


class FakeCambioRepository(ICambioRepository):
    def __init__(self):
        self._cambios = []

    async def crear_cambio(self, cambio: Cambio) -> Cambio:
        self._cambios.append(cambio)
        return cambio

    async def obtener_cambio_por_id(self, cambio_id: str) -> Cambio | None:
        for c in self._cambios:
            if c.id == cambio_id:
                return c
        return None

    async def obtener_cambios_por_venta(self, venta_id: str) -> list[Cambio]:
        return [c for c in self._cambios if c.venta_original_id == venta_id]

    async def actualizar_cambio(self, cambio: Cambio) -> Cambio:
        for i, c in enumerate(self._cambios):
            if c.id == cambio.id:
                self._cambios[i] = cambio
                return cambio

        raise CambioNoEncontradoError(cambio.id)

    def obtener_cambios(self):
        return self._cambios
