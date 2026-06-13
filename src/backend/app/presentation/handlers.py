# Manejadore Globales de Excepciones HU-01, HU-05 y HU-02

from app.domain.exceptions import (
    DescuentoExcedeLimiteError,
    DomainException,
    EstadoProductoInvalidoError,
    PlazoDeCambioVencidoError,  # Nuevo para HU-02
    ProductoNoEncontradoError,
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
    """
    # ... (Manejadores anteriores de HU-01 y HU-05 se mantienen aquí) ...

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

    @app.exception_handler(DomainException)
    async def dominio_generico_handler(request: Request, exc: DomainException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponse(
                error="ERROR_DE_DOMINIO", mensaje=str(exc)
            ).model_dump(),
        )
