from typing import List, Optional

from app.domain.exceptions import (
    EstadoProductoInvalidoError,
    ProductoNoEncontradoError,
    StockInsuficienteError,
)
from app.domain.models.producto import Producto
from app.domain.ports.i_producto_repository import IProductoRepository
from app.infrastructure.database.orm_models.producto_orm import ProductoORM
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession


class ProductoRepository(IProductoRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def obtener_por_codigo(self, codigo: str) -> Optional[Producto]:
        stmt = select(ProductoORM).where(ProductoORM.codigo == codigo)
        result = await self.session.execute(stmt)
        orm_producto = result.scalar_one_or_none()

        if not orm_producto:
            return None

        return self._map_to_domain(orm_producto)

    async def obtener_por_id(self, producto_id: str) -> Optional[Producto]:
        stmt = (
            select(ProductoORM).where(ProductoORM.id == producto_id).with_for_update()
        )
        result = await self.session.execute(stmt)
        orm_producto = result.scalar_one_or_none()

        if not orm_producto:
            return None

        return self._map_to_domain(orm_producto)

    async def actualizar_stock(self, producto_id: str, nuevo_stock: int) -> None:
        stmt = (
            select(ProductoORM).where(ProductoORM.id == producto_id).with_for_update()
        )
        result = await self.session.execute(stmt)
        orm_producto = result.scalar_one_or_none()

        if not orm_producto:
            raise ProductoNoEncontradoError(producto_id)

        if orm_producto.estado != "ACTIVO":
            raise EstadoProductoInvalidoError(producto_id, orm_producto.estado)

        if nuevo_stock < 0:
            raise StockInsuficienteError(
                producto_id,
                orm_producto.nombre,
                orm_producto.stock_actual,
                orm_producto.stock_actual + abs(nuevo_stock),
            )

        orm_producto.stock_actual = nuevo_stock
        # Nota: El commit se delega al Unit of Work (HU-08) para garantizar atomicidad.

    # --- NUEVO MÉTODO PARA HU-06 ---
    async def buscar_por_nombre_o_codigo(self, query: str) -> List[Producto]:
        """
        Busca productos que coincidan con la consulta.
        Prioriza coincidencia exacta en código y coincidencia parcial (case-insensitive) en nombre.
        """
        # Normalizamos la consulta para evitar problemas de espacios
        query_normalizada = query.strip()

        stmt = (
            select(ProductoORM)
            .where(
                or_(
                    ProductoORM.codigo == query_normalizada,
                    ProductoORM.nombre.ilike(f"%{query_normalizada}%"),
                )
            )
            .order_by(ProductoORM.nombre)
        )  # Ordenamos alfabéticamente para mejor UX

        result = await self.session.execute(stmt)
        orm_productos = result.scalars().all()

        return [self._map_to_domain(orm_prod) for orm_prod in orm_productos]

    # --- MÉTODO AUXILIAR DE MAPEO (DRY) ---
    def _map_to_domain(self, orm_producto: ProductoORM) -> Producto:
        """Mapea una instancia ORM a una Entidad de Dominio pura."""
        return Producto(
            id=orm_producto.id,
            codigo=orm_producto.codigo,
            nombre=orm_producto.nombre,
            stock_actual=orm_producto.stock_actual,
            estado=orm_producto.estado,
        )
