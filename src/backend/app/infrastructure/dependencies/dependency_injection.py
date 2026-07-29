from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.consultar_stock_producto_use_case import (
    ConsultarStockProductoUseCase,
)
from app.application.use_cases.validar_stock_venta_use_case import ValidarStockVentaUseCase
from app.domain.ports.i_producto_repository import IProductoRepository
from app.domain.ports.i_venta_repository import IVentaRepository
from app.infrastructure.database.repositories.producto_repository import ProductoRepository
from app.infrastructure.database.repositories.venta_repository import VentaRepository
from app.infrastructure.database.session import get_async_session


def get_producto_repository(
    session: AsyncSession = Depends(get_async_session),
) -> IProductoRepository:
    """Fábrica transient para el repositorio de productos."""
    return ProductoRepository(session=session)


def get_venta_repository(
    session: AsyncSession = Depends(get_async_session),
) -> IVentaRepository:
    """Fábrica transient para el repositorio de ventas."""
    return VentaRepository(session=session)


def get_consultar_stock_producto_use_case(
    producto_repo: IProductoRepository = Depends(get_producto_repository),
) -> ConsultarStockProductoUseCase:
    """Fábrica del caso de uso de consulta de stock."""
    return ConsultarStockProductoUseCase(producto_repository=producto_repo)


def get_validar_stock_venta_use_case(
    producto_repo: IProductoRepository = Depends(get_producto_repository),
    venta_repo: IVentaRepository = Depends(get_venta_repository),
) -> ValidarStockVentaUseCase:
    """Fábrica del caso de uso con inyección por contratos del dominio."""
    return ValidarStockVentaUseCase(
        producto_repository=producto_repo,
        venta_repository=venta_repo,
    )

