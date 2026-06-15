from typing import List, Optional

from app.domain.exceptions import (
    EstadoProductoInvalidoError,
    ProductoNoEncontradoError,
    StockInsuficienteError,
)
from app.domain.models.producto import Producto
from app.domain.ports.i_producto_repository import IProductoRepository


class FakeProductoRepository(IProductoRepository):
    def __init__(self):
        self._productos: dict[str, Producto] = {}

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

    # --- NUEVO MÉTODO PARA HU-06 ---
    async def buscar_por_nombre_o_codigo(self, query: str) -> List[Producto]:
        query_norm = query.strip().lower()
        resultados = []
        for p in self._productos.values():
            # Simula: código exacto OR nombre contiene (case-insensitive)
            if p.codigo == query or query_norm in p.nombre.lower():
                resultados.append(p)

        # Simula el ordenamiento alfabético por nombre
        return sorted(resultados, key=lambda x: x.nombre)
