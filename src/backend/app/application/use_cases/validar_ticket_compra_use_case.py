from app.application.dtos.cambio_dto import ConsultarVentaPorTicketQuery
from app.domain.exceptions import TicketNoEncontradoError
from app.domain.models.detalle_venta import DetalleVenta
from app.domain.ports.i_producto_repository import IProductoRepository
from app.domain.ports.i_venta_repository import IVentaRepository

MENSAJE_TICKET_VALIDO = "Ticket válido. Puede continuar con el proceso de cambio."


class ValidarTicketCompraUseCase:
    """
    Caso de Uso HU-04: valida la existencia de un ticket de compra y devuelve
    los datos de la venta original para iniciar el flujo de cambio.
    """

    def __init__(
        self,
        venta_repository: IVentaRepository,
        producto_repository: IProductoRepository,
    ):
        self._venta_repository = venta_repository
        self._producto_repository = producto_repository

    async def execute(self, query: ConsultarVentaPorTicketQuery) -> dict:
        """Valida que el ticket exista y arma el resumen de la compra.

        Args:
            query: Contiene el numero_ticket ingresado por el cajero.

        Returns:
            Dict con la forma del contrato HU-04: existe, numero_ticket,
            fecha_compra, cajero_original_id, items (con nombre y precio)
            y mensaje.

        Raises:
            TicketNoEncontradoError: Si ningún ticket coincide en el sistema.
        """
        venta = await self._venta_repository.obtener_venta_por_numero_ticket(
            query.numero_ticket
        )

        if venta is None:
            raise TicketNoEncontradoError(query.numero_ticket)

        items = [await self._armar_item(item) for item in venta.items]

        return {
            "existe": True,
            "venta_original_id": venta.id,
            "numero_ticket": venta.numero_ticket,
            "fecha_compra": venta.fecha_hora,
            "cajero_original_id": venta.vendedor_id,
            "items": items,
            "mensaje": MENSAJE_TICKET_VALIDO,
        }

    async def _armar_item(self, item: DetalleVenta) -> dict[str, object]:
        """Resuelve el nombre vigente del producto para un ítem vendido.

        Args:
            item: Detalle de venta con producto_id, cantidad y precio congelado.

        Returns:
            Dict con producto_id, nombre, cantidad y precio del ítem.
        """
        producto = await self._producto_repository.obtener_por_id(item.producto_id)

        return {
            "producto_id": item.producto_id,
            "nombre": producto.nombre if producto else f"Producto {item.producto_id}",
            "cantidad": item.cantidad,
            "precio": item.precio_unitario,
        }
