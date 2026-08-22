from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.exceptions import TicketDuplicadoError
from app.domain.models.detalle_venta import DetalleVenta
from app.domain.models.venta import Venta
from app.domain.ports.i_venta_repository import IVentaRepository
from app.infrastructure.database.orm_models.detalle_venta_orm import DetalleVentaORM
from app.infrastructure.database.orm_models.venta_orm import VentaORM


class VentaRepository(IVentaRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def crear_venta(self, venta: Venta) -> Venta:
        # Mapeo de Entidad de Dominio a ORM
        orm_venta = VentaORM(
            id=venta.id,
            fecha_hora=venta.fecha_hora,
            vendedor_id=venta.vendedor_id,
            estado=venta.estado,
            numero_ticket=venta.numero_ticket,
            total=venta.total,
        )

        for item in venta.items:
            orm_detalle = DetalleVentaORM(
                venta_id=venta.id,
                producto_id=item.producto_id,
                cantidad=item.cantidad,
                precio_unitario=item.precio_unitario,
            )
            orm_venta.detalles.append(orm_detalle)

        self.session.add(orm_venta)
        try:
            await self.session.commit()
        except IntegrityError as exc:
            # La BD rechaza duplicados por el UNIQUE de numero_ticket;
            # se traduce a una excepción de dominio.
            await self.session.rollback()
            mensaje_tecnico = str(exc.orig) if exc.orig else str(exc)
            if "numero_ticket" in mensaje_tecnico:
                raise TicketDuplicadoError(venta.numero_ticket) from exc
            raise

        # Los identificadores se generan del lado cliente y la entidad de
        # dominio ya contiene todos los datos persistidos, por lo que no es
        # necesario refrescar el ORM (evita lazy loads fuera del greenlet).
        return Venta(
            id=venta.id,
            fecha_hora=venta.fecha_hora,
            vendedor_id=venta.vendedor_id,
            estado=venta.estado,
            numero_ticket=venta.numero_ticket,
            total=venta.total,
            items=[
                DetalleVenta(
                    producto_id=item.producto_id,
                    cantidad=item.cantidad,
                    precio_unitario=item.precio_unitario,
                )
                for item in venta.items
            ],
        )
