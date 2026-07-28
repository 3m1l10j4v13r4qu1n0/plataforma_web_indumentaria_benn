from typing import Optional

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.exceptions import (
    ProductoInvalidoError,
    ProductoNoEncontradoError,
    StockInsuficienteError,
)
from app.domain.models.producto import EstadoProducto, Producto
from app.domain.ports.i_producto_repository import IProductoRepository
from app.infrastructure.database.orm_models.producto_orm import ProductoORM


class ProductoRepository(IProductoRepository):
    """Implementación concreta de IProductoRepository con AsyncSession.

    Attributes:
        session: Sesión asíncrona de SQLAlchemy inyectada.
    """

    def __init__(self, session: AsyncSession):
        """Inicializa el repositorio.

        Args:
            session: Sesión asíncrona de SQLAlchemy.
        """
        self.session = session

    async def obtener_por_codigo(self, codigo: str) -> Optional[Producto]:
        """Busca un producto por su código exacto.

        Args:
            codigo: Código de barras o SKU del producto.

        Returns:
            La entidad Producto si existe, None en caso contrario.
        """
        stmt = select(ProductoORM).where(ProductoORM.codigo == codigo)
        result = await self.session.execute(stmt)
        orm_producto = result.scalar_one_or_none()

        if not orm_producto:
            return None

        return self._map_to_domain(orm_producto)

    async def obtener_por_id(self, producto_id: str) -> Optional[Producto]:
        """Busca un producto por su id, bloqueando la fila para escritura.

        Args:
            producto_id: Identificador único (UUID) del producto.

        Returns:
            La entidad Producto si existe, None en caso contrario.
        """
        # Usamos with_for_update() para bloquear la fila y evitar race conditions al actualizar
        stmt = (
            select(ProductoORM).where(ProductoORM.id == producto_id).with_for_update()
        )
        result = await self.session.execute(stmt)
        orm_producto = result.scalar_one_or_none()

        if not orm_producto:
            return None

        return self._map_to_domain(orm_producto)

    async def actualizar_stock(self, producto_id: str, cantidad: int) -> None:
        """Descuenta stock de un producto delegando la regla al dominio.

        Args:
            producto_id: Identificador único (UUID) del producto.
            cantidad: Cantidad de unidades a descontar.

        Raises:
            ProductoNoEncontradoError: Si el producto no existe.
            StockInsuficienteError: Si no hay stock suficiente o el
                producto no está activo (propagada desde el dominio).
        """
        stmt = (
            select(ProductoORM).where(ProductoORM.id == producto_id).with_for_update()
        )
        result = await self.session.execute(stmt)
        orm_producto = result.scalar_one_or_none()

        if not orm_producto:
            raise ProductoNoEncontradoError(producto_id)

        # La regla de "activo + stock suficiente" vive en el dominio,
        # no se reimplementa acá.
        producto = self._map_to_domain(orm_producto)
        producto.descontar_stock(cantidad)

        orm_producto.stock_actual = producto.stock_actual
        # Nota: El commit se delega al Unit of Work (HU-08) para garantizar atomicidad.

    async def buscar_por_nombre_o_codigo(self, query: str) -> list[Producto]:
        """Busca productos activos que coincidan con la consulta.

        Prioriza coincidencia exacta en código y coincidencia parcial
        (case-insensitive) en nombre. Solo devuelve productos activos,
        según lo requerido por HU-06.

        Args:
            query: Texto de búsqueda (código o nombre parcial).

        Returns:
            Lista de entidades Producto que coinciden, ordenadas por
            nombre.
        """
        query_normalizada = query.strip()

        stmt = (
            select(ProductoORM)
            .where(
                ProductoORM.estado == EstadoProducto.ACTIVO.value,
                or_(
                    ProductoORM.codigo == query_normalizada,
                    ProductoORM.nombre.ilike(f"%{query_normalizada}%"),
                ),
            )
            .order_by(ProductoORM.nombre)
        )

        result = await self.session.execute(stmt)
        orm_productos = result.scalars().all()

        return [self._map_to_domain(orm_prod) for orm_prod in orm_productos]

    def _map_to_domain(self, orm_producto: ProductoORM) -> Producto:
        """Mapea una instancia ORM a una entidad de dominio pura.

        Args:
            orm_producto: Instancia de ProductoORM leída de la base de
                datos.

        Returns:
            La entidad Producto equivalente.
        """
        return Producto(
            id=orm_producto.id,
            codigo=orm_producto.codigo,
            nombre=orm_producto.nombre,
            categoria_id=orm_producto.categoria_id,
            precio=orm_producto.precio,
            stock_actual=orm_producto.stock_actual,
            estado=EstadoProducto(orm_producto.estado),
        )