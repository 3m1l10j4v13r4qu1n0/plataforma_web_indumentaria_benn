from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.domain.exceptions import (
    BusquedaInvalidaError,
    CambioNoEncontradoError,
    CambioPlazoVencidoError,
    CantidadMovimientoInvalidaError,
    DescuentoExcedeLimiteError,
    DescuentoInvalidoError,
    DescuentoSinAutorizacionError,
    DomainException,
    ObservacionesRequeridasError,
    ProductoInvalidoError,
    ProductoNoAptoError,
    ProductoNoEncontradoError,
    StockInsuficienteError,
    StockUpdateException,
    TicketDuplicadoError,
    TicketNoEncontradoError,
    VentaNoEncontradaError,
    VentaYaEnCambioError,
)
from app.presentation.schemas.cambio_schema import (
    CambioErrorResponse,
    ProductoNoAptoErrorResponse,
)
from app.presentation.schemas.venta_schema import (
    ErrorResponse,
    TicketNoEncontradoErrorResponse,
)


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

    @app.exception_handler(ProductoNoAptoError)
    async def producto_no_apto_handler(request: Request, exc: ProductoNoAptoError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=ProductoNoAptoErrorResponse(
                error="PRODUCTO_NO_APTO",
                mensaje="El producto no cumple las condiciones para ser cambiado.",
                motivo=exc.motivo,
                es_apto_para_cambio=False,
            ).model_dump(),
        )

    @app.exception_handler(ObservacionesRequeridasError)
    async def observaciones_requeridas_handler(
        request: Request, exc: ObservacionesRequeridasError
    ):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=ProductoNoAptoErrorResponse(
                error="OBSERVACIONES_REQUERIDAS",
                mensaje=str(exc),
                motivo="OBSERVACIONES_OBLIGATORIAS",
                es_apto_para_cambio=False,
            ).model_dump(),
        )

    @app.exception_handler(TicketNoEncontradoError)
    async def ticket_no_encontrado_handler(
        request: Request, exc: TicketNoEncontradoError
    ):
        # Payload específico del contrato HU-04 para el flujo de cambios.
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=TicketNoEncontradoErrorResponse(
                existe=False,
                error="TICKET_NO_ENCONTRADO",
                mensaje=str(exc),
            ).model_dump(),
        )

    @app.exception_handler(VentaYaEnCambioError)
    async def venta_ya_en_cambio_handler(request: Request, exc: VentaYaEnCambioError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=CambioErrorResponse(
                error="VENTA_YA_EN_CAMBIO",
                mensaje=str(exc),
            ).model_dump(),
        )

    @app.exception_handler(StockUpdateException)
    async def stock_update_handler(request: Request, exc: StockUpdateException):
        # HU-08: falla transaccional al actualizar stock (ej. concurrencia).
        # 409 porque el estado del inventario cambió y la operación no pudo aplicarse.
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=ErrorResponse(
                error="ERROR_ACTUALIZACION_STOCK",
                mensaje=str(exc),
                producto_id=exc.producto_id,
            ).model_dump(),
        )

    @app.exception_handler(CantidadMovimientoInvalidaError)
    async def cantidad_movimiento_invalida_handler(
        request: Request, exc: CantidadMovimientoInvalidaError
    ):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=ErrorResponse(
                error="CANTIDAD_MOVIMIENTO_INVALIDA",
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
