from fastapi import APIRouter, Depends, status

from app.application.dtos.cambio_dto import (
    ConsultarVentaPorTicketQuery,
    ProcesarCambioCommand,
)
from app.application.use_cases.consultar_venta_por_ticket_use_case import (
    ConsultarVentaPorTicketUseCase,
)
from app.application.use_cases.procesar_cambio_use_case import ProcesarCambioUseCase
from app.infrastructure.dependencies.dependency_injection import (
    get_consultar_venta_por_ticket_use_case,
    get_procesar_cambio_use_case,
)
from app.presentation.schemas.cambio_schema import (
    CambioErrorResponse,
    CambioResponse,
    ConsultarVentaPorTicketResponse,
    ProcesarCambioRequest,
)

router = APIRouter(prefix="/api/v1", tags=["Cambios"])


@router.get(
    "/ventas/ticket/{numero_ticket}",
    response_model=ConsultarVentaPorTicketResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar Venta por Ticket (Validación previa)",
)
async def consultar_venta_por_ticket(
    numero_ticket: str,
    use_case: ConsultarVentaPorTicketUseCase = Depends(
        get_consultar_venta_por_ticket_use_case
    ),
):
    """
    Obtiene los datos de la venta original para validar si es elegible para cambio.
    Calcula los días transcurridos desde la fecha de compra.
    """
    query = ConsultarVentaPorTicketQuery(numero_ticket=numero_ticket)
    resultado = await use_case.execute(query)
    return ConsultarVentaPorTicketResponse(**resultado)


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
