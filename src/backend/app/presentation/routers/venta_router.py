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
    "/ventas",
    response_model=VentaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Procesar Venta (Validación y Descuento)",
)
async def procesar_venta(
    request: CrearVentaRequest,
    use_case: ValidarStockVentaUseCase = Depends(get_validar_stock_venta_use_case),
):
    """
    Valida el stock de todos los items. Si es válido, confirma la venta
    y descuenta el inventario en una sola transacción atómica.
    Lanza 409 Conflict si hay stock insuficiente (manejado por handlers.py).
    """
    # Mapeo de Schema Pydantic a DTO de Aplicación
    command = CrearVentaCommand(
        vendedor_id=request.vendedor_id,
        items=[
            ItemVentaDTO(producto_id=item.producto_id, cantidad=item.cantidad)
            for item in request.items
        ],
    )

    # Ejecución del Caso de Uso. Las excepciones de dominio burbujearán automáticamente a handlers.py
    venta = await use_case.execute(command)

    return VentaResponse(
        id=venta.id,
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
