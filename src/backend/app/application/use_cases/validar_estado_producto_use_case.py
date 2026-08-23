from datetime import datetime

from app.application.dtos.cambio_dto import (
    ValidarEstadoProductoCommand,
    ValidarEstadoProductoResult,
)
from app.domain.exceptions import (
    CambioInvalidoError,
    CambioNoEncontradoError,
    ProductoNoAptoError,
)
from app.domain.models.cambio import EstadoCambio
from app.domain.ports.i_cambio_repository import ICambioRepository


class ValidarEstadoProductoUseCase:
    """
    Caso de Uso para validar el estado físico del producto presentado a
    cambio (HU-03).

    Acepta únicamente productos NUEVOS y CON ETIQUETA. Si el producto no es
    apto, registra el rechazo en el cambio (auditoría) y lanza
    ProductoNoAptoError para que burbujee hacia la capa de presentación.
    """

    def __init__(self, cambio_repository: ICambioRepository):
        self._cambio_repository = cambio_repository

    async def execute(
        self, command: ValidarEstadoProductoCommand
    ) -> ValidarEstadoProductoResult:
        # 1. Buscar el cambio sobre el que se realiza la inspección
        cambio = await self._cambio_repository.obtener_cambio_por_id(command.cambio_id)

        if cambio is None:
            raise CambioNoEncontradoError(command.cambio_id)

        # 2. El producto inspeccionado debe ser el registrado en el cambio
        if command.producto_id != cambio.producto_a_cambiar_id:
            raise CambioInvalidoError(
                f"El producto '{command.producto_id}' no corresponde al producto "
                "registrado en el cambio."
            )

        # 3. Registrar los datos de la inspección física
        cambio.estado_producto = command.estado_producto
        cambio.tiene_etiqueta = command.tiene_etiqueta
        cambio.observaciones = command.observaciones
        cambio.fecha_validacion = datetime.now()

        if command.cajero_id:
            cambio.cajero_id = command.cajero_id

        # 4. Aplicar la regla de negocio central (dominio puro)
        motivo_rechazo = cambio.validar_estado_fisico()

        if motivo_rechazo is not None:
            # Registrar el rechazo para auditoría antes de lanzar el error
            cambio.estado = EstadoCambio.RECHAZADO_ESTADO_PRODUCTO
            cambio.motivo = motivo_rechazo
            await self._cambio_repository.actualizar_cambio(cambio)

            raise ProductoNoAptoError(motivo=motivo_rechazo)

        # 5. Producto apto: aprobar y persistir la validación
        cambio.estado = EstadoCambio.APROBADO
        await self._cambio_repository.actualizar_cambio(cambio)

        return ValidarEstadoProductoResult(
            es_apto_para_cambio=True,
            mensaje="Producto validado correctamente. Puede continuar con el cambio.",
        )
