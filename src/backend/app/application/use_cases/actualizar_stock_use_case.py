"""Caso de Uso HU-08: actualización automática, atómica y auditada del stock."""

import uuid
from datetime import UTC, datetime

from app.domain.exceptions import (
    CantidadMovimientoInvalidaError,
    DomainException,
    ProductoNoEncontradoError,
    StockUpdateException,
)
from app.domain.models.movimiento_stock import MovimientoStock, TipoMovimiento
from app.domain.ports.i_movimiento_stock_repository import IMovimientoStockRepository
from app.domain.ports.i_producto_repository import IProductoRepository
from app.domain.ports.i_unit_of_work import IUnitOfWork


class ActualizarStockUseCase:
    """
    Caso de Uso para modificar el stock de un producto de forma atómica.

    Agrupa en una única transacción (Unit of Work) la modificación del
    `stock_actual` y el registro del movimiento de auditoría asociado.
    Las invariantes de negocio (stock nunca negativo, cantidades positivas)
    son responsabilidad de las entidades de dominio.

    Ante cualquier error se hace rollback y se lanza `StockUpdateException`,
    salvo para las excepciones de dominio conocidas (ej. `StockInsuficienteError`),
    que burbujean intactas tras el rollback para preservar su mapeo HTTP.
    """

    def __init__(
        self,
        producto_repository: IProductoRepository,
        movimiento_stock_repository: IMovimientoStockRepository,
        unit_of_work: IUnitOfWork,
    ):
        self._producto_repository = producto_repository
        self._movimiento_stock_repository = movimiento_stock_repository
        self._unit_of_work = unit_of_work

    async def execute(
        self,
        producto_id: str,
        cantidad: int,
        tipo_movimiento: TipoMovimiento,
        documento_referencia_id: str | None = None,
    ) -> int:
        """Actualiza el stock de un producto y registra el movimiento.

        Args:
            producto_id: Identificador del producto afectado.
            cantidad: Unidades físicas movidas; debe ser mayor a cero.
            tipo_movimiento: VENTA descuenta stock; DEVOLUCION o AJUSTE lo incrementan.
            documento_referencia_id: ID de la venta o devolución que origina el
                movimiento (opcional para ajustes manuales).

        Returns:
            El `stock_actual` resultante del producto.

        Raises:
            ProductoNoEncontradoError: Si el producto no existe.
            CantidadMovimientoInvalidaError: Si la cantidad no es mayor a cero.
            StockInsuficienteError: Si una venta deja el stock en negativo.
            ProductoInvalidoError: Si el producto no está activo.
            StockUpdateException: Si falla cualquier paso técnico de la transacción.
        """
        try:
            if cantidad <= 0:
                raise CantidadMovimientoInvalidaError(
                    "La cantidad de unidades movidas debe ser mayor a cero."
                )

            producto = await self._producto_repository.obtener_por_id(producto_id)

            if not producto:
                raise ProductoNoEncontradoError(producto_id)

            if tipo_movimiento is TipoMovimiento.VENTA:
                producto.descontar_stock(cantidad)
            else:
                producto.incrementar_stock(cantidad)

            await self._producto_repository.actualizar_stock(
                producto.id, producto.stock_actual
            )

            movimiento = MovimientoStock.registrar(
                id=str(uuid.uuid4()),
                producto_id=producto_id,
                tipo_movimiento=tipo_movimiento,
                cantidad=cantidad,
                fecha_hora=datetime.now(UTC).replace(tzinfo=None),
                documento_referencia_id=documento_referencia_id,
            )
            await self._movimiento_stock_repository.registrar(movimiento)

            await self._unit_of_work.commit()
        except DomainException:
            await self._unit_of_work.rollback()
            raise
        except Exception as exc:
            await self._unit_of_work.rollback()
            raise StockUpdateException(
                producto_id=producto_id,
                motivo=f"error inesperado durante la actualización ({exc})",
            ) from exc

        return producto.stock_actual
