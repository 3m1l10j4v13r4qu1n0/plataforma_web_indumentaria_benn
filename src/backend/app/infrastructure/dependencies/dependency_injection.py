from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.actualizar_stock_use_case import ActualizarStockUseCase
from app.application.use_cases.aplicar_descuento_use_case import AplicarDescuentoUseCase
from app.application.use_cases.buscar_productos_use_case import BuscarProductosUseCase
from app.application.use_cases.consultar_stock_producto_use_case import (
    ConsultarStockProductoUseCase,
)
from app.application.use_cases.login_use_case import LoginUseCase
from app.application.use_cases.marcar_venta_en_cambio_use_case import (
    MarcarVentaEnCambioUseCase,
)
from app.application.use_cases.procesar_cambio_use_case import ProcesarCambioUseCase
from app.application.use_cases.refresh_token_use_case import RefreshTokenUseCase
from app.application.use_cases.registrar_usuario_use_case import (
    RegistrarUsuarioUseCase,
)
from app.application.use_cases.validar_estado_producto_use_case import (
    ValidarEstadoProductoUseCase,
)
from app.application.use_cases.validar_stock_venta_use_case import (
    ValidarStockVentaUseCase,
)
from app.application.use_cases.validar_ticket_compra_use_case import (
    ValidarTicketCompraUseCase,
)
from app.infrastructure.auth.bcrypt_password_hasher import BcryptPasswordHasher
from app.infrastructure.auth.jwt_token_service import JWTTokenService
from app.infrastructure.database.generador_numero_ticket import GeneradorNumeroTicket
from app.infrastructure.database.repositories.cambio_repository import CambioRepository
from app.infrastructure.database.repositories.descuento_repository import (
    DescuentoRepository,
)
from app.infrastructure.database.repositories.movimiento_stock_repository import (
    MovimientoStockRepository,
)
from app.infrastructure.database.repositories.producto_repository import (
    ProductoRepository,
)
from app.infrastructure.database.repositories.usuario_repository import (
    UsuarioRepository,
)
from app.infrastructure.database.repositories.venta_repository import VentaRepository
from app.infrastructure.database.session import get_async_session
from app.infrastructure.database.unit_of_work import UnitOfWorkSQLAlchemy


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


def get_descuento_repository(
    session: AsyncSession = Depends(get_async_session),
) -> DescuentoRepository:
    """
    Fábrica Transient: Crea una nueva instancia del repositorio de descuentos por cada request.
    """
    return DescuentoRepository(session=session)


def get_cambio_repository(
    session: AsyncSession = Depends(get_async_session),
) -> CambioRepository:
    """
    Fábrica Transient: Crea una nueva instancia del repositorio de cambios por cada request.
    """
    return CambioRepository(session=session)


def get_movimiento_stock_repository(
    session: AsyncSession = Depends(get_async_session),
) -> MovimientoStockRepository:
    """
    Fábrica Transient: Crea una nueva instancia del repositorio de movimientos
    de stock por cada request. Comparte la misma sesión asíncrona que el resto
    de los adaptadores del request (requisito para la atomicidad de HU-08).
    """
    return MovimientoStockRepository(session=session)


def get_unit_of_work(
    session: AsyncSession = Depends(get_async_session),
) -> UnitOfWorkSQLAlchemy:
    """
    Fábrica Transient: Crea el Unit of Work del request sobre la sesión
    compartida, para delimitar transacciones atómicas entre agregados.
    """
    return UnitOfWorkSQLAlchemy(session=session)


def get_actualizar_stock_use_case(
    producto_repo: ProductoRepository = Depends(get_producto_repository),
    movimiento_repo: MovimientoStockRepository = Depends(
        get_movimiento_stock_repository
    ),
    unit_of_work: UnitOfWorkSQLAlchemy = Depends(get_unit_of_work),
) -> ActualizarStockUseCase:
    """
    Fábrica del Caso de Uso HU-08: inyecta los puertos para la actualización
    atómica y auditada del stock. Todos los adaptadores comparten la sesión
    del request, por lo que el commit del UoW abarca las tres operaciones.
    """
    return ActualizarStockUseCase(
        producto_repository=producto_repo,
        movimiento_stock_repository=movimiento_repo,
        unit_of_work=unit_of_work,
    )


def get_validar_stock_venta_use_case(
    producto_repo: ProductoRepository = Depends(get_producto_repository),
    venta_repo: VentaRepository = Depends(get_venta_repository),
    generador_ticket: GeneradorNumeroTicket = Depends(get_generador_numero_ticket),
    movimiento_repo: MovimientoStockRepository = Depends(
        get_movimiento_stock_repository
    ),
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
        movimiento_stock_repository=movimiento_repo,
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


def get_consultar_stock_producto_use_case(
    producto_repo: ProductoRepository = Depends(get_producto_repository),
) -> ConsultarStockProductoUseCase:
    """
    Fábrica del Caso de Uso: Inyecta el contrato del repositorio de productos
    en el Caso de Uso de consulta de stock por código. FastAPI se encarga de
    resolver toda la cadena de dependencias por request.
    """
    return ConsultarStockProductoUseCase(producto_repository=producto_repo)


def get_aplicar_descuento_use_case(
    descuento_repo: DescuentoRepository = Depends(get_descuento_repository),
    venta_repo: VentaRepository = Depends(get_venta_repository),
    producto_repo: ProductoRepository = Depends(get_producto_repository),
) -> AplicarDescuentoUseCase:
    """
    Fábrica del Caso de Uso: Inyecta los contratos para el caso de uso de descuentos.
    FastAPI se encarga de resolver toda la cadena de dependencias por request.
    """
    return AplicarDescuentoUseCase(
        descuento_repository=descuento_repo,
        venta_repository=venta_repo,
        producto_repository=producto_repo,
    )


def get_procesar_cambio_use_case(
    cambio_repo: CambioRepository = Depends(get_cambio_repository),
    venta_repo: VentaRepository = Depends(get_venta_repository),
    producto_repo: ProductoRepository = Depends(get_producto_repository),
) -> ProcesarCambioUseCase:
    """
    Fábrica del Caso de Uso: Inyecta los contratos para procesar un cambio de producto.
    """
    return ProcesarCambioUseCase(
        cambio_repository=cambio_repo,
        venta_repository=venta_repo,
        producto_repository=producto_repo,
    )


def get_validar_estado_producto_use_case(
    cambio_repo: CambioRepository = Depends(get_cambio_repository),
) -> ValidarEstadoProductoUseCase:
    """
    Fábrica del Caso de Uso: Inyecta el contrato del repositorio de cambios
    para la validación del estado físico del producto (HU-03).
    """
    return ValidarEstadoProductoUseCase(cambio_repository=cambio_repo)


def get_validar_ticket_compra_use_case(
    venta_repo: VentaRepository = Depends(get_venta_repository),
    producto_repo: ProductoRepository = Depends(get_producto_repository),
) -> ValidarTicketCompraUseCase:
    """
    Fábrica del Caso de Uso: Inyecta los contratos para validar la existencia
    de un ticket de compra e iniciar el flujo de cambio (HU-04).
    """
    return ValidarTicketCompraUseCase(
        venta_repository=venta_repo,
        producto_repository=producto_repo,
    )


def get_marcar_venta_en_cambio_use_case(
    venta_repo: VentaRepository = Depends(get_venta_repository),
) -> MarcarVentaEnCambioUseCase:
    """
    Fábrica del Caso de Uso: Inyecta el contrato del repositorio de ventas
    para retener un ticket en proceso de cambio (HU-04).
    """
    return MarcarVentaEnCambioUseCase(venta_repository=venta_repo)


# ── Fábricas de Autenticación (HU-09) ────────────────────────────────


def get_usuario_repository(
    session: AsyncSession = Depends(get_async_session),
) -> UsuarioRepository:
    """Fábrica Transient: Crea una nueva instancia del repositorio de usuarios."""
    return UsuarioRepository(session=session)


def get_password_hasher() -> BcryptPasswordHasher:
    """Fábrica Singleton: Retorna la instancia de hashing bcrypt."""
    return BcryptPasswordHasher()


def get_token_service() -> JWTTokenService:
    """Fábrica Singleton: Retorna la instancia del servicio JWT."""
    return JWTTokenService()


def get_registrar_usuario_use_case(
    usuario_repo: UsuarioRepository = Depends(get_usuario_repository),
    password_hasher: BcryptPasswordHasher = Depends(get_password_hasher),
) -> RegistrarUsuarioUseCase:
    """Fábrica del Caso de Uso: Registra un usuario nuevo."""
    return RegistrarUsuarioUseCase(
        usuario_repository=usuario_repo,
        password_hasher=password_hasher,
    )


def get_login_use_case(
    usuario_repo: UsuarioRepository = Depends(get_usuario_repository),
    password_hasher: BcryptPasswordHasher = Depends(get_password_hasher),
    token_service: JWTTokenService = Depends(get_token_service),
) -> LoginUseCase:
    """Fábrica del Caso de Uso: Autentica un usuario y emite tokens."""
    return LoginUseCase(
        usuario_repository=usuario_repo,
        password_hasher=password_hasher,
        token_service=token_service,
    )


def get_refresh_token_use_case(
    token_service: JWTTokenService = Depends(get_token_service),
) -> RefreshTokenUseCase:
    """Fábrica del Caso de Uso: Renueva un access token."""
    return RefreshTokenUseCase(token_service=token_service)
