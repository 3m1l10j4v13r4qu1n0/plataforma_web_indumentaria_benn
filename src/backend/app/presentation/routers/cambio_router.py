from fastapi import APIRouter, Depends, status

from app.application.dtos.cambio_dto import (
    ProcesarCambioCommand,
    ValidarEstadoProductoCommand,
)
from app.application.use_cases.procesar_cambio_use_case import ProcesarCambioUseCase
from app.application.use_cases.validar_estado_producto_use_case import (
    ValidarEstadoProductoUseCase,
)
from app.infrastructure.dependencies.dependency_injection import (
    get_procesar_cambio_use_case,
    get_validar_estado_producto_use_case,
)
from app.presentation.schemas.cambio_schema import (
    CambioErrorResponse,
    CambioResponse,
    ProductoNoAptoErrorResponse,
    ProcesarCambioRequest,
    ValidarEstadoProductoRequest,
    ValidarEstadoProductoResponse,
)

router = APIRouter(prefix="/api/v1", tags=["Cambios"])


@router.post(
    "/cambios",
    response_model=CambioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Procesar Cambio de Producto",
    responses={
        status.HTTP_403_FORBIDDEN: {
            "model": CambioErrorResponse,
            "description": "Plazo de 15 días vencido",
        }
    },
)
async def procesar_cambio(
    request: ProcesarCambioRequest,
    use_case: ProcesarCambioUseCase = Depends(get_procesar_cambio_use_case),
):
    """
    Registra el cambio de un producto, validando estrictamente que no hayan pasado
    más de 15 días desde la compra.
    """
    command = ProcesarCambioCommand(
        venta_original_id=request.venta_original_id,
        cajero_id=request.cajero_id,
        producto_a_cambiar_id=request.producto_a_cambiar_id,
        nuevo_producto_id=request.nuevo_producto_id,
        motivo=request.motivo,
    )

    cambio = await use_case.execute(command)

    return CambioResponse(
        id=cambio.id,
        venta_original_id=cambio.venta_original_id,
        fecha_cambio=cambio.fecha_cambio,
        cajero_id=cambio.cajero_id,
        producto_a_cambiar_id=cambio.producto_a_cambiar_id,
        nuevo_producto_id=cambio.nuevo_producto_id,
        estado=cambio.estado,
        motivo=cambio.motivo,
    )


@router.post(
    "/cambios/{cambio_id}/validar-estado",
    response_model=ValidarEstadoProductoResponse,
    status_code=status.HTTP_200_OK,
    summary="Validar Estado Físico del Producto (HU-03)",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": CambioErrorResponse,
            "description": "Cambio no encontrado",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ProductoNoAptoErrorResponse,
            "description": "Producto no apto para el cambio",
        },
    },
)
async def validar_estado_producto(
    cambio_id: str,
    request: ValidarEstadoProductoRequest,
    use_case: ValidarEstadoProductoUseCase = Depends(
        get_validar_estado_producto_use_case
    ),
):
    """
    Valida el estado físico del producto que el cliente desea cambiar (HU-03).
    Solo se aceptan productos NUEVOS y CON ETIQUETA. Si el producto no cumple
    las condiciones, se registra el rechazo y se bloquea el cambio.
    """
    command = ValidarEstadoProductoCommand(
        cambio_id=cambio_id,
        producto_id=request.producto_id,
        estado_producto=request.estado_producto,
        tiene_etiqueta=request.tiene_etiqueta,
        observaciones=request.observaciones,
        cajero_id=request.cajero_id,
    )

    resultado = await use_case.execute(command)

    return ValidarEstadoProductoResponse(
        mensaje=resultado.mensaje,
        es_apto_para_cambio=resultado.es_apto_para_cambio,
    )
