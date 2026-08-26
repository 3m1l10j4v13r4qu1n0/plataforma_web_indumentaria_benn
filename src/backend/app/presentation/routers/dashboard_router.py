from datetime import date, datetime

from fastapi import APIRouter, Depends, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.orm_models.producto_orm import ProductoORM
from app.infrastructure.database.orm_models.venta_orm import VentaORM
from app.infrastructure.database.session import get_async_session
from app.presentation.schemas.dashboard_schema import (
    ProductoStockBajo,
    ResumenDashboard,
)

router = APIRouter(prefix="/api/v1/dashboard", tags=["Dashboard"])

STOCK_BAJO_UMBRAL = 5


@router.get(
    "/resumen",
    response_model=ResumenDashboard,
    status_code=status.HTTP_200_OK,
    summary="Resumen del dashboard principal",
)
async def obtener_resumen(
    session: AsyncSession = Depends(get_async_session),
) -> ResumenDashboard:
    """
    Devuelve métricas resumidas para el dashboard:
    - Cantidad de ventas del día.
    - Total facturado del día.
    - Cantidad de productos con stock bajo (≤ 5 unidades).
    """
    hoy = date.today()
    inicio_del_dia = datetime.combine(hoy, datetime.min.time())
    fin_del_dia = datetime.combine(hoy, datetime.max.time())

    # Ventas del día
    resultado_ventas = await session.execute(
        select(
            func.count(VentaORM.id),
            func.coalesce(func.sum(VentaORM.total), 0),
        ).where(
            VentaORM.fecha_hora >= inicio_del_dia,
            VentaORM.fecha_hora <= fin_del_dia,
        )
    )
    fila_ventas = resultado_ventas.one()
    ventas_hoy = fila_ventas[0]
    total_facturado = float(fila_ventas[1])

    # Productos con stock bajo
    resultado_stock_bajo = await session.execute(
        select(func.count(ProductoORM.id)).where(
            ProductoORM.stock_actual <= STOCK_BAJO_UMBRAL,
            ProductoORM.estado == "ACTIVO",
        )
    )
    productos_stock_bajo = resultado_stock_bajo.scalar() or 0

    return ResumenDashboard(
        ventas_hoy=ventas_hoy,
        total_facturado_hoy=total_facturado,
        productos_stock_bajo=productos_stock_bajo,
    )


@router.get(
    "/productos-stock-bajo",
    response_model=list[ProductoStockBajo],
    status_code=status.HTTP_200_OK,
    summary="Productos con stock bajo",
)
async def productos_stock_bajo(
    session: AsyncSession = Depends(get_async_session),
) -> list[ProductoStockBajo]:
    """
    Devuelve la lista de productos activos con stock ≤ 5 unidades.
    """
    resultado = await session.execute(
        select(ProductoORM)
        .where(
            ProductoORM.stock_actual <= STOCK_BAJO_UMBRAL,
            ProductoORM.estado == "ACTIVO",
        )
        .order_by(ProductoORM.stock_actual.asc())
    )
    productos = resultado.scalars().all()

    return [
        ProductoStockBajo(
            producto_id=p.id,
            codigo=p.codigo,
            nombre=p.nombre,
            stock_actual=p.stock_actual,
        )
        for p in productos
    ]
