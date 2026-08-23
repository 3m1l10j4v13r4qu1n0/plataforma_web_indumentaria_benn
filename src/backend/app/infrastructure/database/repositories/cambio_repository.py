from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.domain.models.cambio import Cambio
from app.domain.ports.i_cambio_repository import ICambioRepository
from app.infrastructure.database.orm_models.cambio_orm import CambioORM


class CambioRepository(ICambioRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def crear_cambio(self, cambio: Cambio) -> Cambio:
        orm_cambio = CambioORM(
            id=cambio.id,
            venta_original_id=cambio.venta_original_id,
            fecha_cambio=cambio.fecha_cambio,
            cajero_id=cambio.cajero_id,
            producto_a_cambiar_id=cambio.producto_a_cambiar_id,
            nuevo_producto_id=cambio.nuevo_producto_id,
            estado=cambio.estado,
            motivo=cambio.motivo,
            fecha_compra_original=cambio.fecha_compra_original,
        )

        self.session.add(orm_cambio)
        await self.session.commit()

        return Cambio(
            id=cambio.id,
            venta_original_id=cambio.venta_original_id,
            fecha_cambio=cambio.fecha_cambio,
            cajero_id=cambio.cajero_id,
            producto_a_cambiar_id=cambio.producto_a_cambiar_id,
            nuevo_producto_id=cambio.nuevo_producto_id,
            estado=cambio.estado,
            motivo=cambio.motivo,
            fecha_compra_original=cambio.fecha_compra_original,
        )

    async def obtener_cambio_por_id(self, cambio_id: str) -> Cambio | None:
        stmt = select(CambioORM).where(CambioORM.id == cambio_id)
        result = await self.session.execute(stmt)
        orm_cambio = result.scalar_one_or_none()

        if orm_cambio is None:
            return None

        return Cambio(
            id=orm_cambio.id,
            venta_original_id=orm_cambio.venta_original_id,
            fecha_cambio=orm_cambio.fecha_cambio,
            cajero_id=orm_cambio.cajero_id,
            producto_a_cambiar_id=orm_cambio.producto_a_cambiar_id,
            nuevo_producto_id=orm_cambio.nuevo_producto_id,
            estado=orm_cambio.estado,
            motivo=orm_cambio.motivo,
            fecha_compra_original=orm_cambio.fecha_compra_original,
        )

    async def obtener_cambios_por_venta(self, venta_id: str) -> list[Cambio]:
        stmt = select(CambioORM).where(CambioORM.venta_original_id == venta_id)
        result = await self.session.execute(stmt)
        orm_cambios = result.scalars().all()

        return [
            Cambio(
                id=orm_cambio.id,
                venta_original_id=orm_cambio.venta_original_id,
                fecha_cambio=orm_cambio.fecha_cambio,
                cajero_id=orm_cambio.cajero_id,
                producto_a_cambiar_id=orm_cambio.producto_a_cambiar_id,
                nuevo_producto_id=orm_cambio.nuevo_producto_id,
                estado=orm_cambio.estado,
                motivo=orm_cambio.motivo,
                fecha_compra_original=orm_cambio.fecha_compra_original,
            )
            for orm_cambio in orm_cambios
        ]
