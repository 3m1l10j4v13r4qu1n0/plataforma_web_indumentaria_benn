from fastapi import APIRouter, Depends, status

from app.application.use_cases.buscar_productos_use_case import BuscarProductosUseCase
from app.domain.models.producto import Producto
from app.domain.models.usuario import Usuario
from app.infrastructure.dependencies.dependency_injection import (
    get_buscar_productos_use_case,
)
from app.presentation.dependencies import get_current_user
from app.presentation.schemas.producto_schema import (
    BuscarProductosResponse,
    ProductoStockResponse,
)

router = APIRouter(prefix="/api/v1/productos", tags=["Productos"])


@router.get(
    "/buscar",
    response_model=BuscarProductosResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
    summary="Buscar productos activos por nombre o código e informar su stock",
)
async def buscar_productos(
    query: str,
    buscar_use_case: BuscarProductosUseCase = Depends(get_buscar_productos_use_case),
    _usuario: Usuario = Depends(get_current_user),
) -> BuscarProductosResponse:
    """
    Busca productos por nombre o código y devuelve su stock actual en tiempo real.

    - La búsqueda es insensible a mayúsculas/minúsculas.
    - Solo devuelve productos en estado ACTIVO.
    - Si el término tiene menos de 3 caracteres responde 400 (manejado por handlers.py).
    - Si no hay coincidencias responde 200 con la lista vacía y un mensaje.
    """
    productos: list[Producto] = await buscar_use_case.execute(query)

    resultados = [
        ProductoStockResponse(
            producto_id=producto.id,
            codigo=producto.codigo,
            nombre=producto.nombre,
            stock_actual=producto.stock_actual,
            estado=producto.estado,
        )
        for producto in productos
    ]

    return BuscarProductosResponse(
        resultados=resultados,
        total_encontrados=len(resultados),
        mensaje=(
            "No se encontraron productos que coincidan con la búsqueda."
            if not resultados
            else None
        ),
    )
