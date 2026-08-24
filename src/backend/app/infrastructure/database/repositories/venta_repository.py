from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.exceptions import TicketDuplicadoError
from app.domain.models.detalle_venta import DetalleVenta
from app.domain.models.venta import EstadoVenta, Venta
from app.domain.ports.i_venta_repository import IVentaRepository
from app.infrastructure.database.orm_models.detalle_venta_orm import DetalleVentaORM
from app.infrastructure.database.orm_models.venta_orm import VentaORM


class VentaRepository(IVentaRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    def _mapear_a_entidad(orm_venta: VentaORM) -> Venta:
        """Convierte una fila ORM de venta (con sus detalles cargados) a entidad de dominio.

        Args:
            orm_venta: Instancia de VentaORM con la relación `detalles` accesible.

        Returns:
            Entidad de dominio Venta equivalente.
        """
        return Venta(
            id=orm_venta.id,
            fecha_hora=orm_venta.fecha_hora,
            vendedor_id=orm_venta.vendedor_id,
            estado=orm_venta.estado,
            numero_ticket=orm_venta.numero_ticket,
            total=orm_venta.total,
            items=[
                DetalleVenta(
                    producto_id=detalle.producto_id,
                    cantidad=detalle.cantidad,
                    precio_unitario=detalle.precio_unitario,
                )
                for detalle in orm_venta.detalles
            ],
        )

    async def obtener_venta_por_id(self, venta_id: str) -> Venta | None:
        stmt = select(VentaORM).where(VentaORM.id == venta_id)
        result = await self.session.execute(stmt)
        orm_venta = result.scalar_one_or_none()

        if orm_venta is None:
            return None

        return self._mapear_a_entidad(orm_venta)

    async def obtener_venta_por_numero_ticket(self, numero_ticket: str) -> Venta | None:
        stmt = select(VentaORM).where(VentaORM.numero_ticket == numero_ticket)
        result = await self.session.execute(stmt)
        orm_venta = result.scalar_one_or_none()

        if orm_venta is None:
            return None

        return self._mapear_a_entidad(orm_venta)

    async def actualizar_estado(
        self, numero_ticket: str, nuevo_estado: EstadoVenta
    ) -> Venta | None:
        """Actualiza el estado de una venta identificada por su número de ticket (HU-04).

        Args:
            numero_ticket: Número de ticket único de la venta.
            nuevo_estado: Estado de destino (ej. EN_CAMBIO).

        Returns:
            La entidad de dominio actualizada, o None si el ticket no existe.
        """
        stmt = select(VentaORM).where(VentaORM.numero_ticket == numero_ticket)
        result = await self.session.execute(stmt)
        orm_venta = result.scalar_one_or_none()

        if orm_venta is None:
            return None

        orm_venta.estado = nuevo_estado
        await self.session.commit()

        return self._mapear_a_entidad(orm_venta)

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
