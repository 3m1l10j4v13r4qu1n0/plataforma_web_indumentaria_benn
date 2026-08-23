from decimal import Decimal

from fastapi import APIRouter, Depends, status

from app.application.dtos.descuento_dto import AplicarDescuentoCommand
from app.application.use_cases.aplicar_descuento_use_case import AplicarDescuentoUseCase
from app.infrastructure.dependencies.dependency_injection import (
    get_aplicar_descuento_use_case,
)
from app.presentation.schemas.descuento_schema import (
    AplicarDescuentoRequest,
    DescuentoResponse,
)

router = APIRouter(prefix="/api/v1", tags=["Descuentos"])


@router.post(
    "/descuentos",
    response_model=DescuentoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Aplicar descuento a una venta (HU-05)",
)
async def aplicar_descuento(
    request: AplicarDescuentoRequest,
    use_case: AplicarDescuentoUseCase = Depends(get_aplicar_descuento_use_case),
):
    """
    Aplica un descuento a una venta existente.

    Reglas de negocio:
    - Descuentos hasta 20%: aprobados automáticamente.
    - Descuentos superiores a 20%: requieren autorización de gerente.
    - Solo se pueden aplicar descuentos a ventas confirmadas.
    - No se permiten múltiples descuentos por venta.

    Lanza 422 ante errores de validación de negocio (manejado por handlers.py).
    """
    # Mapeo de Schema Pydantic a DTO de Aplicación
    command = AplicarDescuentoCommand(
        venta_id=request.venta_id,
        porcentaje=request.porcentaje,
        motivo=request.motivo,
        autorizado_por=request.autorizado_por,
    )

    # Ejecución del Caso de Uso
    descuento = await use_case.execute(command)

    # Determinar si el descuento requería autorización
    requiere_autorizacion = descuento.porcentaje > Decimal("20.0")

    # Construir mensaje según el caso
    mensaje = (
        f"Descuento de {descuento.porcentaje}% aplicado exitosamente. "
        f"Monto descontado: ${descuento.monto_descuento}"
    )
    if requiere_autorizacion:
        mensaje += f" (Autorizado por gerente: {descuento.autorizado_por})"

    return DescuentoResponse(
        id=descuento.id,
        venta_id=descuento.venta_id,
        porcentaje=descuento.porcentaje,
        monto_descuento=descuento.monto_descuento,
        motivo=descuento.motivo,
        autorizado_por=descuento.autorizado_por,
        fecha_aplicacion=descuento.fecha_aplicacion,
        requiere_autorizacion=requiere_autorizacion,
        mensaje=mensaje,
    )
