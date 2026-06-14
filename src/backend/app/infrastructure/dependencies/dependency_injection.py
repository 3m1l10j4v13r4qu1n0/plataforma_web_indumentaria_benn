# Casos de Uso (Aplicación)
from app.application.use_cases.procesar_venta_use_case import ProcesarVentaUseCase
from app.application.use_cases.solicitar_cambio_use_case import (
    SolicitarCambioUseCase,
)  # HU-02 (Paso 4)

# Puertos (Interfaces del Dominio)
from app.domain.ports.i_producto_repository import IProductoRepository
from app.domain.ports.i_usuario_repository import IUsuarioRepository
from app.domain.ports.i_venta_repository import IVentaRepository

# Repositorios Concretos (Infraestructura)
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

# ---------------- FACTORÍAS DE REPOSITORIOS (Ciclo de Vida: Transient) ----------------


def get_producto_repository(
    session: AsyncSession = Depends(get_async_session),
) -> IProductoRepository:
    """Instancia un nuevo repositorio de productos por cada request."""
    return ProductoRepository(session=session)


def get_venta_repository(
    session: AsyncSession = Depends(get_async_session),
) -> IVentaRepository:
    """
    Instancia un nuevo repositorio de ventas por cada request.
    La implementación concreta (VentaRepository) ya satisface el contrato actualizado
    con el método obtener_por_numero_ticket() (HU-02, HU-04).
    """
    return VentaRepository(session=session)


def get_usuario_repository(
    session: AsyncSession = Depends(get_async_session),
) -> IUsuarioRepository:
    """Instancia un nuevo repositorio de usuarios por cada request."""
    return UsuarioRepository(session=session)


# ---------------- FACTORÍAS DE CASOS DE USO ----------------


def get_procesar_venta_use_case(
    producto_repo: IProductoRepository = Depends(get_producto_repository),
    venta_repo: IVentaRepository = Depends(get_venta_repository),
    usuario_repo: IUsuarioRepository = Depends(get_usuario_repository),
) -> ProcesarVentaUseCase:
    """Inyecta los contratos necesarios para HU-01 y HU-05."""
    return ProcesarVentaUseCase(
        producto_repository=producto_repo,
        venta_repository=venta_repo,
        usuario_repository=usuario_repo,
    )


def get_solicitar_cambio_use_case(
    venta_repo: IVentaRepository = Depends(get_venta_repository),
    producto_repo: IProductoRepository = Depends(get_producto_repository),
) -> SolicitarCambioUseCase:
    """
    Fábrica del Caso de Uso de Cambio (HU-02, HU-03, HU-04).
    Inyecta únicamente las abstracciones (Protocol), cumpliendo con la Inversión de Dependencias (DIP).
    Ciclo de vida Transient: se crea una nueva instancia por cada petición HTTP.
    """
    return SolicitarCambioUseCase(
        venta_repository=venta_repo, producto_repository=producto_repo
    )
