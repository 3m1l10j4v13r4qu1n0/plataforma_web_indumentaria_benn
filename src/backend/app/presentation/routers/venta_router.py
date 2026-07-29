from app.application.dtos.venta_dto import CrearVentaCommand, ItemVentaDTO
from app.application.use_cases.consultar_stock_producto_use_case import (
    ConsultarStockProductoUseCase,
)
from app.application.use_cases.validar_stock_venta_use_case import (
    ValidarStockVentaUseCase,
)
from app.infrastructure.dependencies.dependency_injection import (
    get_consultar_stock_producto_use_case,
    get_validar_stock_venta_use_case,
)
from app.presentation.schemas.venta_schema import (
    CrearVentaRequest,
    ItemVentaResponse,
    StockResponse,
    StockSearchResponse,
    VentaResponse,
)
from fastapi import APIRouter, Depends, Query, status

router = APIRouter(prefix="/api/v1", tags=["Ventas y Stock"])


@router.get(
    "/productos/stock",
    response_model=StockSearchResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar Stock en tiempo real",
)
async def consultar_stock(
    query: str = Query(..., description="Nombre o código del producto a buscar"),
    use_case: ConsultarStockProductoUseCase = Depends(
        get_consultar_stock_producto_use_case
    ),
):
    """Busca productos por nombre o código y devuelve su stock disponible."""
    productos = await use_case.execute(query)

    return StockSearchResponse(
        productos=[
            StockResponse(
                producto_id=producto.id,
                nombre=producto.nombre,
                stock_actual=producto.stock_actual,
            )
            for producto in productos
        ],
        mensaje=f"Se encontraron {len(productos)} producto(s) coincidente(s).",
    )


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
    Procesa una venta: valida stock, autoriza descuentos si aplica,
    genera automáticamente un número de ticket único (HU-07) y
    descuenta el inventario de forma atómica (HU-08).

    Las excepciones de dominio burbujean a handlers.py (sin try/except aquí).
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

    # Ejecución del Caso de Uso. Si falla, handlers.py intercepta y responde.
    venta = await use_case.execute(command)

    return VentaResponse(
        id=venta.id,
        numero_ticket=venta.numero_ticket,  # <-- Mapeo explícito del ticket generado (HU-07)
        fecha_hora=venta.fecha_hora,
        vendedor_id=venta.vendedor_id,
        estado=venta.estado,
        items=[
            ItemVentaResponse(
                producto_id=item.producto_id, 
                cantidad=item.cantidad
                ) 
                for item in venta.items
                ]
    )
