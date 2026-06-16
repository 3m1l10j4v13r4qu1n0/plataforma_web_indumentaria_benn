from typing import Optional

from app.domain.models.descuento import Descuento
from app.domain.models.detalle_venta import DetalleVenta
from app.domain.models.venta import Venta
from app.domain.ports.i_venta_repository import IVentaRepository
from app.infrastructure.database.orm_models.detalle_venta_orm import DetalleVentaORM
from app.infrastructure.database.orm_models.venta_orm import VentaORM
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class VentaRepository(IVentaRepository):
    """
    Implementamos el método obtener_por_numero_ticket
    definido en el puerto IVentaRepository. Este método
    recupera la venta y la mapea de vuelta a la Entidad
    de Dominio pura, incluyendo su Objeto de Valor
    Descuento.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def crear_venta(self, venta: Venta) -> Venta:
        orm_venta = VentaORM(
            id=venta.id,
            fecha_hora=venta.fecha_hora,
            vendedor_id=venta.vendedor_id,
            numero_ticket=venta.numero_ticket,
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
        # El commit se delega al Unit of Work (HU-08)
        await self.session.refresh(orm_venta)

        return self._map_to_domain(orm_venta)

    async def obtener_por_numero_ticket(self, numero_ticket: str) -> Optional[Venta]:
        """
        Recupera una venta utilizando su número de comprobante único.
        Devuelve None si no existe, delegando al Caso de Uso la decisión
        de lanzar VentaNoEncontradaError (cumpliendo con el Protocol Optional[Venta]).
        """
        stmt = select(VentaORM).where(VentaORM.numero_ticket == numero_ticket)
        result = await self.session.execute(stmt)
        orm_venta = result.scalar_one_or_none()

        if not orm_venta:
            return None

        return self._map_to_domain(orm_venta)

    # --- DRY: Centralización del mapeo ORM -> Dominio ---
    @staticmethod
    def _map_to_domain(orm_venta: VentaORM) -> Venta:
        return Venta(
            id=orm_venta.id,
            fecha_hora=orm_venta.fecha_hora,
            vendedor_id=orm_venta.vendedor_id,
            numero_ticket=orm_venta.numero_ticket,  # <-- Recuperación HU-07
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
