# app/domain/ports/i_producto_repository.py
from typing import Optional, Protocol

from app.domain.models.producto import Producto


class IProductoRepository(Protocol):
    def obtener_por_codigo(self, codigo: str) -> Optional[Producto]: ...

    def obtener_por_id(self, producto_id: str) -> Optional[Producto]: ...

    def actualizar_stock(self, producto_id: str, nuevo_stock: int) -> None: ...
