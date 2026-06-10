# Importamos el Caso de Uso que se creará en el Paso 4.
# (Se usa importación relativa o absoluta según la estructura final del proyecto)
from app.application.use_cases.validar_stock_venta_use_case import (
    ValidarStockVentaUseCase,
)
from app.infrastructure.database.repositories.producto_repository import (
    ProductoRepository,
)
from app.infrastructure.database.repositories.venta_repository import VentaRepository
from app.infrastructure.database.session import get_async_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


def get_producto_repository(
    session: AsyncSession = Depends(get_async_session),
) -> ProductoRepository:
    """
    Fábrica Transient: Crea una nueva instancia del repositorio por cada request.
    """
    return ProductoRepository(session=session)


def get_venta_repository(
    session: AsyncSession = Depends(get_async_session),
) -> VentaRepository:
    """
    Fábrica Transient: Crea una nueva instancia del repositorio por cada request.
    """
    return VentaRepository(session=session)


def get_validar_stock_venta_use_case(
    producto_repo: ProductoRepository = Depends(get_producto_repository),
    venta_repo: VentaRepository = Depends(get_venta_repository),
) -> ValidarStockVentaUseCase:
    """
    Fábrica del Caso de Uso: Inyecta los contratos (implementados por los repositorios concretos)
    en el Caso de Uso. FastAPI se encarga de resolver toda la cadena de dependencias.
    """
    return ValidarStockVentaUseCase(
        producto_repository=producto_repo, venta_repository=venta_repo
    )
