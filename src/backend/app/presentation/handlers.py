from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.domain.exceptions import (
    BusquedaInvalidaError,
    CambioNoEncontradoError,
    CambioPlazoVencidoError,
    DescuentoExcedeLimiteError,
    DescuentoInvalidoError,
    DescuentoSinAutorizacionError,
    DomainException,
    ProductoInvalidoError,
    ProductoNoEncontradoError,
    StockInsuficienteError,
    TicketDuplicadoError,
    VentaNoEncontradaError,
)
from app.presentation.schemas.cambio_schema import CambioErrorResponse
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
                producto_id=exc.identificador,
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
    async def estado_invalido_handler(request: Request, exc: ProductoInvalidoError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponse(
                error="ESTADO_PRODUCTO_INVALIDO",
                mensaje=str(exc),
                producto_id=exc.producto_id,
            ).model_dump(),
        )

    @app.exception_handler(BusquedaInvalidaError)
    async def busqueda_invalida_handler(request: Request, exc: BusquedaInvalidaError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponse(
                error="BUSQUEDA_INVALIDA",
                mensaje=str(exc),
            ).model_dump(),
        )

    @app.exception_handler(TicketDuplicadoError)
    async def ticket_duplicado_handler(request: Request, exc: TicketDuplicadoError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=ErrorResponse(
                error="TICKET_DUPLICADO",
                mensaje=str(exc),
            ).model_dump(),
        )

    @app.exception_handler(DescuentoExcedeLimiteError)
    async def descuento_excede_limite_handler(
        request: Request, exc: DescuentoExcedeLimiteError
    ):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=ErrorResponse(
                error="DESCUENTO_EXCEDE_LIMITE",
                mensaje=str(exc),
            ).model_dump(),
        )

    @app.exception_handler(DescuentoSinAutorizacionError)
    async def descuento_sin_autorizacion_handler(
        request: Request, exc: DescuentoSinAutorizacionError
    ):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=ErrorResponse(
                error="DESCUENTO_SIN_AUTORIZACION",
                mensaje=str(exc),
            ).model_dump(),
        )

    @app.exception_handler(DescuentoInvalidoError)
    async def descuento_invalido_handler(request: Request, exc: DescuentoInvalidoError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=ErrorResponse(
                error="DESCUENTO_INVALIDO",
                mensaje=str(exc),
            ).model_dump(),
        )

    @app.exception_handler(VentaNoEncontradaError)
    async def venta_no_encontrada_handler(
        request: Request, exc: VentaNoEncontradaError
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=ErrorResponse(
                error="VENTA_NO_ENCONTRADA",
                mensaje=str(exc),
            ).model_dump(),
        )

    @app.exception_handler(CambioPlazoVencidoError)
    async def cambio_plazo_vencido_handler(
        request: Request, exc: CambioPlazoVencidoError
    ):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=CambioErrorResponse(
                error="PLAZO_VENCIDO",
                mensaje=str(exc),
            ).model_dump(),
        )

    @app.exception_handler(CambioNoEncontradoError)
    async def cambio_no_encontrado_handler(
        request: Request, exc: CambioNoEncontradoError
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=CambioErrorResponse(
                error="CAMBIO_NO_ENCONTRADO",
                mensaje=str(exc),
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
