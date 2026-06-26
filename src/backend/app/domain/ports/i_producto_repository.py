from typing import Protocol

from app.domain.models.producto import Producto


class IProductoRepository(Protocol):
    def obtener_por_codigo(self, codigo: str) -> Producto: ...

    def actualizar_stock(self, producto_id: str, nuevo_stock: int) -> None: ...
