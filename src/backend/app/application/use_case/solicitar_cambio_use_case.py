from app.application.dtos.cambio_dto import SolicitarCambioCommand
from app.domain.exceptions import VentaNoEncontradaError
from app.domain.ports.i_venta_repository import IVentaRepository


class SolicitarCambioUseCase:
    """
    Caso de Uso para validar la elegibilidad de una venta para un cambio (HU-02).
    Orquesta la recuperación de la venta y delega la validación de invariantes
    (plazo de 15 días, estado de la venta) a la entidad de dominio.
    """

    def __init__(self, venta_repository: IVentaRepository):
        # DIP: Solo dependemos de la abstracción (Protocol), nunca de la implementación concreta.
        self._venta_repository = venta_repository

    async def execute(self, command: SolicitarCambioCommand) -> dict:
        # 1. Recuperar la venta por su comprobante
        venta = await self._venta_repository.obtener_por_numero_ticket(
            command.numero_ticket
        )

        # 2. Si no existe, la excepción de dominio burbujea (será atrapada en handlers.py)
        if not venta:
            raise VentaNoEncontradaError(command.numero_ticket)

        # 3. Delegar la validación de la regla de negocio a la Entidad de Dominio (SRP)
        # Si el plazo está vencido o el estado no es CONFIRMADA, la entidad lanzará
        # PlazoDeCambioVencidoError o ValueError, respectivamente.
        venta.validar_elegibilidad_para_cambio(command.fecha_solicitud)

        # 4. Retornar un DTO de respuesta o diccionario con los datos validados
        # para que los siguientes pasos del flujo (HU-03, HU-04) puedan continuar.
        return {
            "venta_id": venta.id,
            "numero_ticket": venta.numero_ticket,
            "fecha_compra": venta.fecha_hora,
            "estado": venta.estado,
            "mensaje": "Venta elegible para cambio. Proceda con la validación del estado del producto.",
        }
