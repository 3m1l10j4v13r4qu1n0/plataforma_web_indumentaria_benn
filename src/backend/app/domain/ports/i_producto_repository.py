from typing import Protocol

from app.domain.models.producto import Producto


class IProductoRepository(Protocol):
    async def obtener_por_codigo(self, codigo: str) -> Producto | None: ...

    async def obtener_por_id(self, producto_id: str) -> Producto | None: ...

    async def actualizar_stock(self, producto_id: str, nuevo_stock: int) -> None: ...
