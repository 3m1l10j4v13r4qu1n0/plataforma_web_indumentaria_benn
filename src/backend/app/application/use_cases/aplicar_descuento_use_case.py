import uuid
from datetime import datetime, UTC
from decimal import Decimal

from app.application.dtos.descuento_dto import AplicarDescuentoCommand
from app.domain.exceptions import (
    DescuentoInvalidoError,
    DescuentoSinAutorizacionError,
    DomainException,
)
from app.domain.models.descuento import Descuento
from app.domain.ports.i_descuento_repository import IDescuentoRepository
from app.domain.ports.i_producto_repository import IProductoRepository
from app.domain.ports.i_venta_repository import IVentaRepository


class AplicarDescuentoUseCase:
    """
    Caso de Uso para aplicar descuentos a una venta.
    Implementa las reglas de negocio de la HU-05:
    - Límite máximo de 20% sin autorización
    - Si supera el límite, requiere autorización de gerente
    - Registra auditoría completa del descuento
    """

    # Límite máximo de descuento sin autorización (porcentaje)
    LIMITE_DESCUENTO_SIN_AUTORIZACION = Decimal("20.0")

    def __init__(
        self,
        descuento_repository: IDescuentoRepository,
        venta_repository: IVentaRepository,
        producto_repository: IProductoRepository,
    ):
        self._descuento_repository = descuento_repository
        self._venta_repository = venta_repository
        self._producto_repository = producto_repository

    async def execute(self, command: AplicarDescuentoCommand) -> Descuento:
        # 1. Validar que la venta exista
        venta = await self._venta_repository.obtener_por_id(command.venta_id)
        if not venta:
            raise DomainException(
                f"La venta con ID '{command.venta_id}' no existe en el sistema."
            )

        # 2. Validar que la venta esté confirmada
        if venta.estado != "CONFIRMADA":
            raise DomainException(
                f"La venta '{command.venta_id}' no está confirmada (Estado: {venta.estado}). "
                "Solo se pueden aplicar descuentos a ventas confirmadas."
            )

        # 3. Validar que no exista ya un descuento para esta venta
        descuento_existente = await self._descuento_repository.obtener_por_venta_id(
            command.venta_id
        )
        if descuento_existente:
            raise DomainException(
                f"Ya existe un descuento registrado para la venta '{command.venta_id}'. "
                "No se pueden aplicar múltiples descuentos a una misma venta."
            )

        # 4. Validar el porcentaje del descuento
        if command.porcentaje <= 0 or command.porcentaje > 100:
            raise DescuentoInvalidoError(
                f"El porcentaje {command.porcentaje}% no es válido. Debe estar entre 0 y 100."
            )

        # 5. Verificar si requiere autorización
        requiere_autorizacion = command.porcentaje > self.LIMITE_DESCUENTO_SIN_AUTORIZACION

        if requiere_autorizacion and not command.autorizado_por:
            raise DescuentoSinAutorizacionError(float(command.porcentaje))

        # 6. Calcular el monto de descuento
        monto_descuento = (venta.total * command.porcentaje) / Decimal("100")

        # 7. Crear la entidad de dominio
        descuento_id = str(uuid.uuid4())
        fecha_actual = datetime.now(UTC).replace(tzinfo=None)

        nuevo_descuento = Descuento(
            id=descuento_id,
            venta_id=command.venta_id,
            porcentaje=command.porcentaje,
            monto_descuento=monto_descuento,
            motivo=command.motivo,
            autorizado_por=command.autorizado_por,
            fecha_aplicacion=fecha_actual,
        )

        # 8. Persistir el descuento
        descuento_guardado = await self._descuento_repository.crear_descuento(
            nuevo_descuento
        )

        return descuento_guardado
