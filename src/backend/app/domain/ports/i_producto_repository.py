from typing import Protocol

from app.domain.models.producto import Producto


class IProductoRepository(Protocol):
    async def obtener_por_codigo(self, codigo: str) -> Producto: ...

    async def obtener_por_id(self, producto_id: str) -> Producto: ...

    async def actualizar_stock(self, producto_id: str, nuevo_stock: int) -> None: ...

    # --- Nuevo contrato para HU-06 ---
    async def buscar_por_nombre_o_codigo(self, query: str) -> list[Producto]:
        """
        Busca productos que coincidan con la consulta.
        La implementación en infraestructura debe manejar la lógica de 
        coincidencia (ej: ILIKE para nombre, o igualdad para código).
        """
        ...