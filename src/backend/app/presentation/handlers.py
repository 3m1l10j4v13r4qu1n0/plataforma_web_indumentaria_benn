from app.domain.exceptions import (
    DescuentoExcedeLimiteError,
    DomainException,
    EstadoProductoInvalidoError,
    PlazoDeCambioVencidoError,  # Nuevo para HU-02
    ProductoNoAptoParaCambioError,  # Nuevo para HU-03
    ProductoNoEncontradoError,
    ProductoNoPerteneceAVentaError,  # Nuevo para HU-04
    StockInsuficienteError,
    UsuarioNoAutorizadoError,
    VentaNoEncontradaError,  # Nuevo para HU-02/04
)
from app.presentation.schemas.cambio_schema import ErrorResponse
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


def register_exception_handlers(app: FastAPI):
    """
    Registra los manejadores de excepciones de dominio en la aplicación FastAPI.
    Esto garantiza que los routers permanezcan limpios de bloques try/except.
    """

    # HU-01
    @app.exception_handler(ProductoNoEncontradoError)
    async def producto_no_encontrado_handler(
        request: Request, exc: ProductoNoEncontradoError
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=ErrorResponse(
                error="PRODUCTO_NO_ENCONTRADO",
                mensaje=str(exc),
                producto_id=exc.codigo if hasattr(exc, "codigo") else exc.producto_id,
            ).model_dump(),
        )

    @app.exception_handler(StockInsuficienteError)
    async def stock_insuficiente_handler(request: Request, exc: StockInsuficienteError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=ErrorResponse(
                error="STOCK_INSUFICIENTE",
                mensaje=exc.__str__(),  # Usa el mensaje detallado de la excepción
                producto_id=exc.producto_id,
            ).model_dump(),
        )

    @app.exception_handler(EstadoProductoInvalidoError)
    async def estado_invalido_handler(
        request: Request, exc: EstadoProductoInvalidoError
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponse(
                error="ESTADO_PRODUCTO_INVALIDO",
                mensaje=str(exc),
                producto_id=exc.producto_id,
            ).model_dump(),
        )

    # HU-05
    @app.exception_handler(DescuentoExcedeLimiteError)
    async def descuento_excede_limite_handler(
        request: Request, exc: DescuentoExcedeLimiteError
    ):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,  # 403 indica que la acción está prohibida sin la debida autorización
            content=ErrorResponse(
                error="DESCUENTO_EXCEDE_LIMITE", mensaje=str(exc)
            ).model_dump(),
        )

    @app.exception_handler(UsuarioNoAutorizadoError)
    async def usuario_no_autorizado_handler(
        request: Request, exc: UsuarioNoAutorizadoError
    ):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=ErrorResponse(
                error="USUARIO_NO_AUTORIZADO",
                mensaje=str(exc),
                usuario_id=exc.usuario_id,
            ).model_dump(),
        )

    # HU-02
    @app.exception_handler(VentaNoEncontradaError)
    async def venta_no_encontrada_handler(
        request: Request, exc: VentaNoEncontradaError
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=ErrorResponse(
                error="VENTA_NO_ENCONTRADA",
                mensaje=str(exc),
                numero_ticket=exc.identificador,
            ).model_dump(),
        )

    @app.exception_handler(PlazoDeCambioVencidoError)
    async def plazo_cambio_vencido_handler(
        request: Request, exc: PlazoDeCambioVencidoError
    ):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,  # 403 indica que la acción está prohibida por reglas de negocio
            content=ErrorResponse(
                error="PLAZO_DE_CAMBIO_VENCIDO",
                mensaje=str(exc),
                numero_ticket=exc.numero_ticket,
            ).model_dump(),
        )

    # HU-03 y HU-04
    @app.exception_handler(ProductoNoAptoParaCambioError)
    async def producto_no_apto_handler(
        request: Request, exc: ProductoNoAptoParaCambioError
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,  # 400 indica que la solicitud viola una regla de negocio de estado
            content=ErrorResponse(
                error="PRODUCTO_NO_APTO_PARA_CAMBIO", mensaje=str(exc)
            ).model_dump(),
        )

    @app.exception_handler(ProductoNoPerteneceAVentaError)
    async def producto_no_pertenece_handler(
        request: Request, exc: ProductoNoPerteneceAVentaError
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponse(
                error="PRODUCTO_NO_PERTENECE_A_VENTA",
                mensaje=str(exc),
                producto_id=exc.producto_id,
                numero_ticket=exc.numero_ticket,
            ).model_dump(),
        )

    @app.exception_handler(DomainException)
    async def dominio_generico_handler(request: Request, exc: DomainException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponse(
                error="ERROR_DE_DOMINIO", mensaje=str(exc)
            ).model_dump(),
        )
