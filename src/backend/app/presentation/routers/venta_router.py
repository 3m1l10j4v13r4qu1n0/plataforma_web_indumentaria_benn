"""
Router API REST
Actualizamos el endpoint para recivir nuevos capos y
mapearlos al CrearVentaCommand HU-01 y HU-05

"""

from app.application.dtos.venta_dto import CrearVentaCommand, ItemVentaDTO
from app.application.use_cases.procesar_venta_use_case import ProcesarVentaUseCase
from app.domain.ports.i_producto_repository import IProductoRepository
from app.infrastructure.dependencies.dependency_injection import (
    get_procesar_venta_use_case,
    get_producto_repository,
)
from app.presentation.schemas.venta_schema import (
    CrearVentaRequest,
    StockResponse,
    VentaResponse,
)
from fastapi import APIRouter, Depends, status

router = APIRouter(prefix="/api/v1", tags=["Ventas y Stock"])


@router.get(
    "/productos/{codigo}/stock",
    response_model=StockResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar Stock en tiempo real",
)
async def consultar_stock(
    codigo: str, producto_repo: IProductoRepository = Depends(get_producto_repository)
):
    producto = await producto_repo.obtener_por_codigo(codigo)
    if not producto:
        from app.domain.exceptions import ProductoNoEncontradoError

        raise ProductoNoEncontradoError(codigo)

    return StockResponse(
        producto_id=producto.id,
        nombre=producto.nombre,
        stock_actual=producto.stock_actual,
    )


@router.post(
    "/ventas",
    response_model=VentaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Procesar Venta (Validación Stock + Descuentos)",
)
async def procesar_venta(
    request: CrearVentaRequest,
    use_case: ProcesarVentaUseCase = Depends(get_procesar_venta_use_case),
):
    """
    Valida el stock de todos los items y la autorización de descuentos.
    Si es válido, confirma la venta y descuenta el inventario en una sola transacción.
    """
    # Mapeo de Schema Pydantic a DTO de Aplicación
    command = CrearVentaCommand(
        vendedor_id=request.vendedor_id,
        items=[
            ItemVentaDTO(producto_id=item.producto_id, cantidad=item.cantidad)
            for item in request.items
        ],
        porcentaje_descuento=request.porcentaje_descuento,
        gerente_autorizacion_id=request.gerente_autorizacion_id,
    )

    # Ejecución del Caso de Uso. Las excepciones de dominio burbujearán automáticamente a handlers.py
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
