# Inyeccion de Dependencias HU-01 y HU-05

# Importación anticipada del Caso de Uso que se creará en el Paso 4
from app.application.use_cases.procesar_venta_use_case import ProcesarVentaUseCase

# Puertos (Interfaces) para Type Hinting en los getters
from app.domain.ports.i_producto_repository import IProductoRepository
from app.domain.ports.i_usuario_repository import IUsuarioRepository
from app.domain.ports.i_venta_repository import IVentaRepository

# Repositorios Concretos
from app.infrastructure.database.repositories.producto_repository import (
    ProductoRepository,
)
from app.infrastructure.database.repositories.usuario_repository import (
    UsuarioRepository,
)
from app.infrastructure.database.repositories.venta_repository import VentaRepository
from app.infrastructure.database.session import get_async_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


def get_producto_repository(
    session: AsyncSession = Depends(get_async_session),
) -> IProductoRepository:
    """
    Fábrica Transient: Provee una instancia del repositorio de productos por request.
    Retorna la interfaz IProductoRepository para favorecer la Inversión de Dependencias.
    """
    return ProductoRepository(session=session)


def get_venta_repository(
    session: AsyncSession = Depends(get_async_session),
) -> IVentaRepository:
    """
    Fábrica Transient: Provee una instancia del repositorio de ventas por request.
    """
    return VentaRepository(session=session)


def get_usuario_repository(
    session: AsyncSession = Depends(get_async_session),
) -> IUsuarioRepository:
    """
    Fábrica Transient: Provee una instancia del repositorio de usuarios por request.
    """
    return UsuarioRepository(session=session)


def get_procesar_venta_use_case(
    producto_repo: IProductoRepository = Depends(get_producto_repository),
    venta_repo: IVentaRepository = Depends(get_venta_repository),
    usuario_repo: IUsuarioRepository = Depends(get_usuario_repository),
) -> ProcesarVentaUseCase:
    """
    Fábrica del Caso de Uso de Venta:
    Inyecta los tres contratos necesarios para cumplir con HU-01 (Stock) y HU-05 (Descuentos).
    FastAPI resuelve recursivamente todas las dependencias (incluyendo la sesión de BD).
    """
    return ProcesarVentaUseCase(
        producto_repository=producto_repo,
        venta_repository=venta_repo,
        usuario_repository=usuario_repo,
    )
