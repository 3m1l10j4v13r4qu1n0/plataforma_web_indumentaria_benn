from datetime import datetime

from app.application.dtos.cambio_dto import ItemCambioDTO, SolicitarCambioCommand
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
    summary="Validar elegibilidad de venta y productos para cambio (HU-02, HU-03, HU-04)",
)
async def validar_elegibilidad_cambio(
    request: SolicitarCambioRequest,
    use_case: SolicitarCambioUseCase = Depends(get_solicitar_cambio_use_case),
):
    """
    Valida si una venta y sus productos específicos son elegibles para cambio verificando:
    1. Que el ticket exista y la venta esté CONFIRMADA (HU-02, HU-04).
    2. Que no hayan transcurrido más de 15 días calendario (HU-02).
    3. Que cada producto solicitado pertenezca a ese ticket (HU-04).
    4. Que la condición declarada de cada producto sea 'NUEVO_CON_ETIQUETA' (HU-03).

    Si falla, el manejador global (handlers.py) intercepta la excepción de dominio
    y devuelve el código HTTP correspondiente (400, 403 o 404).
    """
    command = SolicitarCambioCommand(
        numero_ticket=request.numero_ticket,
        fecha_solicitud=datetime.utcnow(),
        items_a_cambiar=[
            ItemCambioDTO(
                producto_id=item.producto_id,
                condicion_declarada=item.condicion_declarada,
            )
            for item in request.items_a_cambiar
        ],
    )

    # Ejecución del Caso de Uso. Las excepciones burbujearán automáticamente a handlers.py
    resultado = await use_case.execute(command)

    return ElegibilidadCambioResponse(**resultado)
