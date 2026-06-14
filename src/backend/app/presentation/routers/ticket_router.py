from app.application.use_cases.consultar_ticket_use_case import ConsultarTicketUseCase
from app.infrastructure.dependencies.dependency_injection import (
    get_consultar_ticket_use_case,
)
from app.presentation.schemas.ticket_schema import TicketDetalleResponse
from fastapi import APIRouter, Depends, status

router = APIRouter(prefix="/api/v1/ventas", tags=["Ventas y Tickets"])


@router.get(
    "/tickets/{numero_ticket}",
    response_model=TicketDetalleResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar detalles de un ticket de compra (HU-04)",
)
async def consultar_ticket(
    numero_ticket: str,
    use_case: ConsultarTicketUseCase = Depends(get_consultar_ticket_use_case),
):
    """
    Recupera los detalles de una venta utilizando su número de comprobante.
    Fundamental para iniciar el flujo de cambios (HU-02, HU-03).
    Si no existe, el handler global devuelve 404 Not Found.
    """
    # Sin try/except. La excepción VentaNoEncontradaError burbujea a handlers.py
    return await use_case.execute(numero_ticket)
