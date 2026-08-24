from app.application.dtos.cambio_dto import ConsultarVentaPorTicketQuery
from app.application.dtos.venta_dto import CrearVentaCommand, ItemVentaDTO
from app.application.use_cases.consultar_stock_producto_use_case import (
    ConsultarStockProductoUseCase,
)
from app.application.use_cases.marcar_venta_en_cambio_use_case import (
    MarcarVentaEnCambioCommand,
    MarcarVentaEnCambioUseCase,
)
from app.application.use_cases.validar_stock_venta_use_case import (
    ValidarStockVentaUseCase,
)
from app.application.use_cases.validar_ticket_compra_use_case import (
    ValidarTicketCompraUseCase,
)
from app.domain.models.venta import EstadoVenta
from app.infrastructure.dependencies.dependency_injection import (
    get_consultar_stock_producto_use_case,
    get_marcar_venta_en_cambio_use_case,
    get_validar_stock_venta_use_case,
    get_validar_ticket_compra_use_case,
)
from app.presentation.schemas.venta_schema import (
    CrearVentaRequest,
    ItemTicketResponse,
    ItemVentaResponse,
    MarcarEnCambioResponse,
    StockResponse,
    TicketNoEncontradoErrorResponse,
    ValidarTicketResponse,
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


@router.get(
    "/ventas/validar-ticket/{numero_ticket}",
    response_model=ValidarTicketResponse,
    status_code=status.HTTP_200_OK,
    summary="Validar existencia de ticket de compra (HU-04)",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": TicketNoEncontradoErrorResponse,
            "description": "El número de ticket ingresado no existe en el sistema",
        }
    },
)
async def validar_ticket_compra(
    numero_ticket: str,
    use_case: ValidarTicketCompraUseCase = Depends(get_validar_ticket_compra_use_case),
):
    """
    Verifica si un ticket existe en el sistema y devuelve los datos de la
    compra original para iniciar el flujo de cambio (HU-04).
    """
    query = ConsultarVentaPorTicketQuery(numero_ticket=numero_ticket)
    resultado = await use_case.execute(query)

    return ValidarTicketResponse(
        existe=True,
        numero_ticket=resultado["numero_ticket"],
        fecha_compra=resultado["fecha_compra"],
        cajero_original_id=resultado["cajero_original_id"],
        items=[
            ItemTicketResponse(
                producto_id=item["producto_id"],
                nombre=item["nombre"],
                cantidad=item["cantidad"],
                precio=float(item["precio"]),
            )
            for item in resultado["items"]
        ],
        mensaje=resultado["mensaje"],
    )


@router.patch(
    "/ventas/{numero_ticket}/estado",
    response_model=MarcarEnCambioResponse,
    status_code=status.HTTP_200_OK,
    summary="Marcar venta como EN_CAMBIO (HU-04)",
)
async def marcar_venta_en_cambio(
    numero_ticket: str,
    use_case: MarcarVentaEnCambioUseCase = Depends(get_marcar_venta_en_cambio_use_case),
):
    """
    Retiene el ticket cambiando su estado a EN_CAMBIO, evitando que dos cajeros
    procesen el mismo ticket simultáneamente en diferentes cajas.
    Lanza 404 si el ticket no existe y 409 si ya está en proceso de cambio.
    """
    command = MarcarVentaEnCambioCommand(numero_ticket=numero_ticket)
    venta = await use_case.execute(command)

    return MarcarEnCambioResponse(
        numero_ticket=venta.numero_ticket,
        estado=EstadoVenta(venta.estado).value,
        mensaje="Venta marcada como EN_CAMBIO. El ticket queda retenido para esta caja.",
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
