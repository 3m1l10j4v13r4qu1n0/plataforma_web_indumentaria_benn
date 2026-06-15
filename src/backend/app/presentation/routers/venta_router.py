from app.application.dtos.venta_dto import CrearVentaCommand, ItemVentaDTO
from app.application.use_cases.procesar_venta_use_case import ProcesarVentaUseCase
from app.infrastructure.dependencies.dependency_injection import (
    get_procesar_venta_use_case,
)
from app.presentation.schemas.venta_schema import (
    CrearVentaRequest,
    ItemVentaResponse,
    VentaResponse,
)
from fastapi import APIRouter, Depends, status

router = APIRouter(prefix="/api/v1/ventas", tags=["Ventas"])


@router.post(
    "",
    response_model=VentaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Procesar Venta (Validación Stock + Descuentos)",
)
async def procesar_venta(
    request: CrearVentaRequest,
    use_case: ProcesarVentaUseCase = Depends(get_procesar_venta_use_case),
):
    """
    Valida stock, autoriza descuentos y procesa la venta.
    Internamente (HU-08), descuenta el stock y registra el MovimientoStock
    en una sola transacción atómica (ACID).

    Cero bloques try/except. Las excepciones de dominio burbujean a handlers.py.
    """
    command = CrearVentaCommand(
        vendedor_id=request.vendedor_id,
        items=[
            ItemVentaDTO(producto_id=item.producto_id, cantidad=item.cantidad)
            for item in request.items
        ],
        porcentaje_descuento=request.porcentaje_descuento,
        gerente_autorizacion_id=request.gerente_autorizacion_id,
    )

    venta = await use_case.execute(command)

    return VentaResponse(
        id=venta.id,
        fecha_hora=venta.fecha_hora,
        vendedor_id=venta.vendedor_id,
        estado=venta.estado,
        items=[
            ItemVentaResponse(producto_id=item.producto_id, cantidad=item.cantidad)
            for item in venta.items
        ],
        descuento={
            "porcentaje": venta.descuento.porcentaje,
            "gerente_autorizacion_id": venta.descuento.gerente_autorizacion_id,
        },
    )
