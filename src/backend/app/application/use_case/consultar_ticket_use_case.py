from app.application.dtos.ticket_dto import ItemTicketDTO, TicketDetalleDTO
from app.domain.exceptions import VentaNoEncontradaError
from app.domain.ports.i_venta_repository import IVentaRepository


class ConsultarTicketUseCase:
    """
    Caso de Uso para consultar los detalles de un comprobante de venta (HU-04).
    """

    def __init__(self, venta_repository: IVentaRepository):
        self._venta_repository = venta_repository

    async def execute(self, numero_ticket: str) -> TicketDetalleDTO:
        venta = await self._venta_repository.obtener_por_numero_ticket(numero_ticket)

        if not venta:
            raise VentaNoEncontradaError(numero_ticket)

        # Mapeo de Entidad de Dominio a DTO de Aplicación
        return TicketDetalleDTO(
            numero_ticket=venta.numero_ticket,
            fecha_hora=venta.fecha_hora,
            vendedor_id=venta.vendedor_id,
            estado=venta.estado,
            items=[
                # Nota: Para obtener el nombre del producto, idealmente el repositorio
                # debería hacer un join o el caso de uso consultar IProductoRepository.
                # Por simplicidad y bajo acoplamiento, asumimos que el nombre se resuelve
                # en la capa de presentación o se denormaliza en el DTO de venta.
                # Aquí usamos un placeholder o el ID si no tenemos el nombre en el agregado.
                ItemTicketDTO(
                    producto_id=item.producto_id,
                    nombre=f"Producto {item.producto_id}",  # Se enriquecería con IProductoRepository si es estrictamente necesario
                    cantidad=item.cantidad,
                )
                for item in venta.items
            ],
        )
