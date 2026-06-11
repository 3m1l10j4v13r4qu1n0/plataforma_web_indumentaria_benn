# Manejadore Globales de Excepciones HU-01 y HU-05

from app.domain.exceptions import (
    DescuentoExcedeLimiteError,  # Nuevo
    DomainException,
    EstadoProductoInvalidoError,
    ProductoNoEncontradoError,
    StockInsuficienteError,
    UsuarioNoAutorizadoError,  # Nuevo
)
from app.presentation.schemas.venta_schema import ErrorResponse
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


def register_exception_handlers(app: FastAPI):
    """
    Registra los manejadores de excepciones de dominio en la aplicación FastAPI.
    """

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
                mensaje=str(exc),
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

    # --- Nuevos Manejadores para HU-05 ---
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

    # -------------------------------------

    @app.exception_handler(DomainException)
    async def dominio_generico_handler(request: Request, exc: DomainException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponse(
                error="ERROR_DE_DOMINIO", mensaje=str(exc)
            ).model_dump(),
        )
