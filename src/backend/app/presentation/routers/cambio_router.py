"""
El router se limita a recibir la petición, validar el esquema Pydantic, invocar el
Caso de Uso y devolver la respuesta. Cero bloques try/except.

"""

from datetime import datetime

from app.application.dtos.cambio_dto import SolicitarCambioCommand
from app.application.use_cases.solicitar_cambio_use_case import SolicitarCambioUseCase
from app.infrastructure.dependencies.dependency_injection import (
    get_solicitar_cambio_use_case,
)
from app.presentation.schemas.cambio_schema import (
    ElegibilidadCambioResponse,
    SolicitarCambioRequest,
)
from fastapi import APIRouter, Depends, status

router = APIRouter(prefix="/api/v1/cambios", tags=["Cambios y Devoluciones"])


@router.post(
    "/validar-elegibilidad",
    response_model=ElegibilidadCambioResponse,
    status_code=status.HTTP_200_OK,
    summary="Validar elegibilidad de una venta para cambio (HU-02)",
)
async def validar_elegibilidad_cambio(
    request: SolicitarCambioRequest,
    use_case: SolicitarCambioUseCase = Depends(get_solicitar_cambio_use_case),
):
    """
    Valida si una venta es elegible para cambio verificando:
    1. Que el ticket exista en el sistema.
    2. Que la venta esté en estado CONFIRMADA.
    3. Que no hayan transcurrido más de 15 días calendario desde la compra.

    Si falla, el manejador global (handlers.py) intercepta la excepción de dominio
    y devuelve el código HTTP correspondiente (404 o 403).
    """
    command = SolicitarCambioCommand(
        numero_ticket=request.numero_ticket, fecha_solicitud=datetime.utcnow()
    )

    # Ejecución del Caso de Uso. Las excepciones burbujearán automáticamente a handlers.py
    resultado = await use_case.execute(command)

    return ElegibilidadCambioResponse(**resultado)
