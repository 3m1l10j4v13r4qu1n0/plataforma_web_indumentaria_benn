from datetime import datetime

from app.application.dtos.cambio_dto import ConsultarVentaPorTicketQuery
from app.domain.exceptions import VentaNoEncontradaError
from app.domain.ports.i_venta_repository import IVentaRepository


class ConsultarVentaPorTicketUseCase:
    """
    Caso de Uso para consultar una venta por su número de ticket.
    Calcula los días transcurridos y si es elegible para cambio.
    """

    DIAS_LIMITE_CAMBIO = 15

    def __init__(self, venta_repository: IVentaRepository):
        self._venta_repository = venta_repository

    async def execute(self, query: ConsultarVentaPorTicketQuery) -> dict:
        venta = await self._venta_repository.obtener_venta_por_numero_ticket(
            query.numero_ticket
        )

        if venta is None:
            raise VentaNoEncontradaError(query.numero_ticket)

        fecha_actual = datetime.now()
        diferencia = fecha_actual - venta.fecha_hora
        dias_transcurridos = diferencia.days
        es_elegible = dias_transcurridos <= self.DIAS_LIMITE_CAMBIO

        return {
            "numero_ticket": venta.numero_ticket,
            "fecha_compra": venta.fecha_hora,
            "dias_transcurridos": dias_transcurridos,
            "es_elegible_para_cambio": es_elegible,
            "items": [
                {
                    "producto_id": item.producto_id,
                    "cantidad": item.cantidad,
                }
                for item in venta.items
            ],
        }
