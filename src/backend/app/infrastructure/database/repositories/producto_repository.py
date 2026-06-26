from typing import Optional

from app.domain.exceptions import (
    ProductoInvalidoError,
    ProductoNoEncontradoError,
    StockInsuficienteError,
)
from app.domain.models.producto import Producto
from app.domain.ports.i_producto_repository import IProductoRepository
from app.infrastructure.database.orm_models.producto_orm import ProductoORM
from sqlalchemy import select
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

        return Producto(
            id=orm_producto.id,
            codigo=orm_producto.codigo,
            nombre=orm_producto.nombre,
            stock_actual=orm_producto.stock_actual,
            estado=orm_producto.estado,
        )

    async def obtener_por_id(self, producto_id: str) -> Optional[Producto]:
        # Usamos with_for_update() para bloquear la fila y evitar race conditions al actualizar
        stmt = (
            select(ProductoORM).where(ProductoORM.id == producto_id).with_for_update()
        )
        result = await self.session.execute(stmt)
        orm_producto = result.scalar_one_or_none()

        if not orm_producto:
            return None

        return Producto(
            id=orm_producto.id,
            codigo=orm_producto.codigo,
            nombre=orm_producto.nombre,
            stock_actual=orm_producto.stock_actual,
            estado=orm_producto.estado,
        )

    async def actualizar_stock(self, producto_id: str, nuevo_stock: int) -> None:
        stmt = (
            select(ProductoORM).where(ProductoORM.id == producto_id).with_for_update()
        )
        result = await self.session.execute(stmt)
        orm_producto = result.scalar_one_or_none()

        if not orm_producto:
            raise ProductoNoEncontradoError(producto_id)

        if orm_producto.estado != "ACTIVO":
            raise ProductoInvalidoError(producto_id, orm_producto.estado)

        if nuevo_stock < 0:
            # La restricción CHECK de la BD lo atraparía, pero lo validamos a nivel de dominio primero
            raise StockInsuficienteError(
                producto_id,
                orm_producto.nombre,
                orm_producto.stock_actual,
                orm_producto.stock_actual
                + abs(nuevo_stock),  # Cantidad solicitada estimada
            )

        orm_producto.stock_actual = nuevo_stock
        await self.session.commit()
