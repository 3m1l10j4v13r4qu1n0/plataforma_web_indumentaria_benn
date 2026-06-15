from app.application.dtos.producto_dto import BuscarProductosCommand
from app.application.use_cases.buscar_productos_use_case import BuscarProductosUseCase
from app.domain.exceptions import ProductoNoEncontradoError
from app.domain.ports.i_producto_repository import IProductoRepository
from app.infrastructure.dependencies.dependency_injection import (
    get_buscar_productos_use_case,
    get_producto_repository,
)
from app.presentation.schemas.producto_schema import (
    BuscarProductosResponseSchema,
    ProductoStockResumenSchema,
    StockResponse,
)
from fastapi import APIRouter, Depends, Query, status

router = APIRouter(prefix="/api/v1/productos", tags=["Productos y Stock"])


@router.get(
    "/buscar",
    response_model=BuscarProductosResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Buscar productos por nombre o código (HU-06)",
)
async def buscar_productos(
    query: str = Query(
        ...,
        min_length=2,
        description="Término de búsqueda (código exacto o fragmento de nombre)",
    ),
    use_case: BuscarProductosUseCase = Depends(get_buscar_productos_use_case),
):
    """
    Busca productos disponibles en el inventario coincidiendo con el término de búsqueda.
    Permite búsqueda exacta por código o coincidencia parcial (case-insensitive) por nombre.

    Siempre devuelve 200 OK. Si no hay coincidencias, la lista 'productos' estará vacía
    y el 'mensaje' indicará que no se encontraron resultados.
    """
    command = BuscarProductosCommand(query=query)
    resultado = await use_case.execute(command)

    return BuscarProductosResponseSchema(
        productos=[
            ProductoStockResumenSchema(
                producto_id=p.producto_id,
                codigo=p.codigo,
                nombre=p.nombre,
                stock_actual=p.stock_actual,
                estado=p.estado,
            )
            for p in resultado.productos
        ],
        mensaje=resultado.mensaje,
    )


@router.get(
    "/{codigo}/stock",
    response_model=StockResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar stock en tiempo real (HU-07)",
)
async def consultar_stock(
    codigo: str,
    producto_repo: IProductoRepository = Depends(get_producto_repository),
):
    """
    Retorna el stock actual de un producto dado su código exacto.
    Lanza ProductoNoEncontradoError (404) si el código no existe.
    La excepción burbujea a handlers.py — sin try/except aquí.
    """
    producto = await producto_repo.obtener_por_codigo(codigo)
    if not producto:
        raise ProductoNoEncontradoError(codigo)

    return StockResponse(
        producto_id=producto.id,
        nombre=producto.nombre,
        stock_actual=producto.stock_actual,
    )
