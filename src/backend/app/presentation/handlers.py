from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.domain.exceptions import (
    DomainException,
    ProductoInvalidoError,
    ProductoNoEncontradoError,
    StockInsuficienteError,
)
from app.presentation.schemas.venta_schema import ErrorResponse


def register_exception_handlers(app: FastAPI):
    """
    Registra los manejadores de excepciones de dominio en la aplicación FastAPI.
    Esto garantiza que los routers permanezcan limpios de bloques try/except.
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
                mensaje=exc.__str__(),  # Usa el mensaje detallado de la excepción
                producto_id=exc.producto_id,
            ).model_dump(),
        )

    @app.exception_handler(ProductoInvalidoError)
    async def estado_invalido_handler(
        request: Request, exc: ProductoInvalidoError
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponse(
                error="ESTADO_PRODUCTO_INVALIDO",
                mensaje=str(exc),
                producto_id=exc.producto_id,
            ).model_dump(),
        )

    @app.exception_handler(DomainException)
    async def dominio_generico_handler(request: Request, exc: DomainException):
        # Fallback para cualquier otra excepción de dominio no mapeada específicamente
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponse(
                error="ERROR_DE_DOMINIO", mensaje=str(exc)
            ).model_dump(),
        )
