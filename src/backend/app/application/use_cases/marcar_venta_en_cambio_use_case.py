from dataclasses import dataclass

from app.domain.exceptions import (
    DomainException,
    TicketNoEncontradoError,
    VentaYaEnCambioError,
)
from app.domain.models.venta import EstadoVenta, Venta
from app.domain.ports.i_venta_repository import IVentaRepository


@dataclass
class MarcarVentaEnCambioCommand:
    """Datos necesarios para retener un ticket en proceso de cambio (HU-04)."""

    numero_ticket: str


class MarcarVentaEnCambioUseCase:
    """
    Caso de Uso HU-04: marca una venta como EN_CAMBIO para evitar que dos
    cajeros procesen el mismo ticket simultáneamente en distintas cajas.
    """

    def __init__(self, venta_repository: IVentaRepository):
        self._venta_repository = venta_repository

    async def execute(self, command: MarcarVentaEnCambioCommand) -> Venta:
        """Retiene el ticket cambiando el estado de la venta a EN_CAMBIO.

        Args:
            command: Contiene el numero_ticket a retener.

        Returns:
            La entidad Venta actualizada con estado EN_CAMBIO.

        Raises:
            TicketNoEncontradoError: Si el ticket no existe en el sistema.
            VentaYaEnCambioError: Si el ticket ya está retenido por otra caja.
            DomainException: Si la venta no está en estado CONFIRMADA.
        """
        venta = await self._venta_repository.obtener_venta_por_numero_ticket(
            command.numero_ticket
        )

        if venta is None:
            raise TicketNoEncontradoError(command.numero_ticket)

        if venta.estado is EstadoVenta.EN_CAMBIO:
            raise VentaYaEnCambioError(command.numero_ticket)

        if venta.estado is not EstadoVenta.CONFIRMADA:
            raise DomainException(
                "Solo las ventas confirmadas pueden entrar en proceso de cambio."
            )

        return await self._venta_repository.actualizar_estado(
            command.numero_ticket, EstadoVenta.EN_CAMBIO
        )
