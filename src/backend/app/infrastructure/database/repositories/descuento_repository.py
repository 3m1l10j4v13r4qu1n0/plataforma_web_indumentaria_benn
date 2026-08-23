from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.descuento import Descuento
from app.domain.ports.i_descuento_repository import IDescuentoRepository
from app.infrastructure.database.orm_models.descuento_orm import DescuentoORM


class DescuentoRepository(IDescuentoRepository):
    """Implementación concreta del repositorio de descuentos usando SQLAlchemy."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def crear_descuento(self, descuento: Descuento) -> Descuento:
        orm_descuento = DescuentoORM(
            id=descuento.id,
            venta_id=descuento.venta_id,
            porcentaje=descuento.porcentaje,
            monto_descuento=descuento.monto_descuento,
            motivo=descuento.motivo,
            autorizado_por=descuento.autorizado_por,
            fecha_aplicacion=descuento.fecha_aplicacion,
        )

        self.session.add(orm_descuento)
        await self.session.commit()

        return Descuento(
            id=descuento.id,
            venta_id=descuento.venta_id,
            porcentaje=descuento.porcentaje,
            monto_descuento=descuento.monto_descuento,
            motivo=descuento.motivo,
            autorizado_por=descuento.autorizado_por,
            fecha_aplicacion=descuento.fecha_aplicacion,
        )

    async def obtener_por_venta_id(self, venta_id: str) -> Descuento | None:
        result = await self.session.execute(
            select(DescuentoORM).where(DescuentoORM.venta_id == venta_id)
        )
        orm_descuento = result.scalar_one_or_none()

        if not orm_descuento:
            return None

        return self._mapear_a_dominio(orm_descuento)

    async def obtener_por_id(self, descuento_id: str) -> Descuento | None:
        result = await self.session.execute(
            select(DescuentoORM).where(DescuentoORM.id == descuento_id)
        )
        orm_descuento = result.scalar_one_or_none()

        if not orm_descuento:
            return None

        return self._mapear_a_dominio(orm_descuento)

    def _mapear_a_dominio(self, orm_descuento: DescuentoORM) -> Descuento:
        return Descuento(
            id=orm_descuento.id,
            venta_id=orm_descuento.venta_id,
            porcentaje=orm_descuento.porcentaje,
            monto_descuento=orm_descuento.monto_descuento,
            motivo=orm_descuento.motivo,
            autorizado_por=orm_descuento.autorizado_por,
            fecha_aplicacion=orm_descuento.fecha_aplicacion,
        )
