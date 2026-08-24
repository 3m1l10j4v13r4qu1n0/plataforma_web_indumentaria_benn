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
    StockResponse,
    VentaResponse,
    ItemVentaResponse,
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
    codigo: str,
    use_case: ConsultarStockProductoUseCase = Depends(
        get_consultar_stock_producto_use_case
    ),
):
    """
    Obtiene el stock actual de un producto específico por su código.
    Lanza 404 si el producto no existe (manejado por handlers.py).
    """
    producto = await use_case.execute(codigo)

    return StockResponse(
        producto_id=producto.id,
        categoria=producto.categoria,
        nombre=producto.nombre,
        precio=producto.precio,
        stock_actual=producto.stock_actual,
    )


@router.post(
    "/ventas",
    response_model=VentaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Finalizar venta y generar ticket (HU-01 / HU-07)",
)
async def procesar_venta(
    request: CrearVentaRequest,
    use_case: ValidarStockVentaUseCase = Depends(get_validar_stock_venta_use_case),
):
    """
    Valida el stock de todos los items. Si es válido, confirma la venta,
    genera el número de ticket único, calcula el total con los precios
    congelados y descuenta el inventario.
    Lanza 409 Conflict si hay stock insuficiente o ticket duplicado,
    y 404/400 ante productos inexistentes o inactivos (manejado por handlers.py).
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
    resultado = await use_case.execute(command)

    return VentaResponse(
        id=resultado.id,
        fecha_hora=resultado.fecha_hora,
        vendedor_id=resultado.vendedor_id,
        estado=resultado.estado,
        numero_ticket=resultado.numero_ticket,
        total=float(resultado.total) if resultado.total is not None else None,
        mensaje="Venta registrada y ticket generado exitosamente.",
        items=[
            ItemVentaResponse(
                producto_id=item.producto_id,
                nombre=item.nombre,
                cantidad=item.cantidad,
                precio=float(item.precio_unitario),
            )
            for item in resultado.items
        ],
    )
