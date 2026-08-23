import uuid
from datetime import datetime

from app.application.dtos.cambio_dto import ProcesarCambioCommand
from app.domain.exceptions import (
    CambioPlazoVencidoError,
    VentaNoEncontradaError,
)
from app.domain.models.cambio import Cambio, EstadoCambio
from app.domain.ports.i_cambio_repository import ICambioRepository
from app.domain.ports.i_producto_repository import IProductoRepository
from app.domain.ports.i_venta_repository import IVentaRepository


class ProcesarCambioUseCase:
    """
    Caso de Uso para procesar un cambio de producto.
    Valida que la venta exista, que esté dentro del plazo de 15 días,
    y registra el cambio.
    """

    DIAS_LIMITE_CAMBIO = 15

    def __init__(
        self,
        cambio_repository: ICambioRepository,
        venta_repository: IVentaRepository,
        producto_repository: IProductoRepository,
    ):
        self._cambio_repository = cambio_repository
        self._venta_repository = venta_repository
        self._producto_repository = producto_repository

    async def execute(self, command: ProcesarCambioCommand) -> Cambio:
        # 1. Buscar la venta original
        venta = await self._venta_repository.obtener_venta_por_id(
            command.venta_original_id
        )

        if venta is None:
            raise VentaNoEncontradaError(command.venta_original_id)

        # 2. Validar el plazo de 15 días
        fecha_actual = datetime.now()
        diferencia = fecha_actual - venta.fecha_hora
        dias_transcurridos = diferencia.days

        if dias_transcurridos > self.DIAS_LIMITE_CAMBIO:
            raise CambioPlazoVencidoError(
                numero_ticket=venta.numero_ticket or "",
                dias_transcurridos=dias_transcurridos,
                dias_limite=self.DIAS_LIMITE_CAMBIO,
            )

        # 3. Crear el registro del cambio
        cambio_id = str(uuid.uuid4())
        nuevo_cambio = Cambio(
            id=cambio_id,
            venta_original_id=command.venta_original_id,
            fecha_cambio=fecha_actual,
            cajero_id=command.cajero_id,
            producto_a_cambiar_id=command.producto_a_cambiar_id,
            nuevo_producto_id=command.nuevo_producto_id,
            estado=EstadoCambio.APROBADO,
            motivo=command.motivo,
            fecha_compra_original=venta.fecha_hora,
        )

        # 4. Guardar el cambio
        cambio_guardado = await self._cambio_repository.crear_cambio(nuevo_cambio)

        return cambio_guardado
