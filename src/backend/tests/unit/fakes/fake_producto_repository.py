from typing import Dict, Optional

from app.domain.exceptions import (
    EstadoProductoInvalidoError,
    ProductoNoEncontradoError,
    StockInsuficienteError,
)
from app.domain.models.producto import Producto
from app.domain.ports.i_producto_repository import IProductoRepository


class FakeProductoRepository(IProductoRepository):
    def __init__(self):
        self._productos: Dict[str, Producto] = {}

    def agregar_producto(self, producto: Producto):
        self._productos[producto.id] = producto

    async def obtener_por_codigo(self, codigo: str) -> Optional[Producto]:
        for p in self._productos.values():
            if p.codigo == codigo:
                return p
        return None

    async def obtener_por_id(self, producto_id: str) -> Optional[Producto]:
        return self._productos.get(producto_id)

    async def actualizar_stock(self, producto_id: str, nuevo_stock: int) -> None:
        producto = self._productos.get(producto_id)
        if not producto:
            raise ProductoNoEncontradoError(producto_id)

        if producto.estado != "ACTIVO":
            raise EstadoProductoInvalidoError(producto_id, producto.estado)

        if nuevo_stock < 0:
            raise StockInsuficienteError(
                producto_id,
                producto.nombre,
                producto.stock_actual,
                producto.stock_actual + abs(nuevo_stock),
            )

        producto.stock_actual = nuevo_stock
