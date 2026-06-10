# HU-05

from app.domain.models.descuento import Descuento
from app.domain.models.detalle_venta import DetalleVenta
from app.domain.models.venta import Venta
from app.domain.ports.i_venta_repository import IVentaRepository
from app.infrastructure.database.orm_models.detalle_venta_orm import DetalleVentaORM
from app.infrastructure.database.orm_models.venta_orm import VentaORM
from sqlalchemy.ext.asyncio import AsyncSession


class VentaRepository(IVentaRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def crear_venta(self, venta: Venta) -> Venta:
        # Mapeo de Entidad de Dominio a ORM, incluyendo el Value Object Descuento
        orm_venta = VentaORM(
            id=venta.id,
            fecha_hora=venta.fecha_hora,
            vendedor_id=venta.vendedor_id,
            estado=venta.estado,
            porcentaje_descuento=venta.descuento.porcentaje,
            gerente_autorizacion_id=venta.descuento.gerente_autorizacion_id,
        )

        for item in venta.items:
            orm_detalle = DetalleVentaORM(
                venta_id=venta.id, producto_id=item.producto_id, cantidad=item.cantidad
            )
            orm_venta.detalles.append(orm_detalle)

        self.session.add(orm_venta)
        await self.session.commit()
        await self.session.refresh(orm_venta)

        # Reconstrucción de la entidad de dominio desde la BD (incluyendo el Value Object)
        return Venta(
            id=orm_venta.id,
            fecha_hora=orm_venta.fecha_hora,
            vendedor_id=orm_venta.vendedor_id,
            estado=orm_venta.estado,
            items=[
                DetalleVenta(producto_id=d.producto_id, cantidad=d.cantidad)
                for d in orm_venta.detalles
            ],
            descuento=Descuento(
                porcentaje=orm_venta.porcentaje_descuento,
                gerente_autorizacion_id=orm_venta.gerente_autorizacion_id,
            ),
        )
