from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.buscar_productos_use_case import BuscarProductosUseCase
from app.application.use_cases.validar_stock_venta_use_case import (
    ValidarStockVentaUseCase,
)
from app.infrastructure.database.generador_numero_ticket import GeneradorNumeroTicket
from app.infrastructure.database.repositories.producto_repository import (
    ProductoRepository,
)

from app.infrastructure.database.repositories.venta_repository import VentaRepository
from app.infrastructure.database.session import get_async_session


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


def get_generador_numero_ticket(
    session: AsyncSession = Depends(get_async_session),
) -> GeneradorNumeroTicket:
    """
    Fábrica Transient: Crea una nueva instancia del generador por cada request.
    Comparte la misma sesión asíncrona que los repositorios del request.
    """
    return GeneradorNumeroTicket(session=session)


def get_validar_stock_venta_use_case(
    producto_repo: ProductoRepository = Depends(get_producto_repository),
    venta_repo: VentaRepository = Depends(get_venta_repository),
    generador_ticket: GeneradorNumeroTicket = Depends(get_generador_numero_ticket),
) -> ValidarStockVentaUseCase:
    """
    Fábrica del Caso de Uso: Inyecta los contratos (implementados por los adaptadores
    concretos) en el Caso de Uso. FastAPI se encarga de resolver toda la cadena
    de dependencias.
    """
    return ValidarStockVentaUseCase(
        producto_repository=producto_repo,
        venta_repository=venta_repo,
        generador_numero_ticket=generador_ticket,
    )


def get_buscar_productos_use_case(
    producto_repo: ProductoRepository = Depends(get_producto_repository),
) -> BuscarProductosUseCase:
    """
    Fábrica del Caso de Uso: Inyecta el contrato del repositorio de productos
    en el Caso de Uso de búsqueda. FastAPI se encarga de resolver toda la
    cadena de dependencias por request.
    """
    return BuscarProductosUseCase(producto_repository=producto_repo)
