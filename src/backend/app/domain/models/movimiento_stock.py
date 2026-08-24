"""Entidad de dominio MovimientoStock: registro de auditoría de cambios de stock."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from app.domain.exceptions import CantidadMovimientoInvalidaError


class TipoMovimiento(str, Enum):
    """Tipos de movimiento que modifican el stock de un producto."""

    VENTA = "VENTA"
    DEVOLUCION = "DEVOLUCION"
    AJUSTE = "AJUSTE"


@dataclass
class MovimientoStock:
    """Registro de auditoría que documenta por qué cambió el stock de un producto.

    La cantidad se almacena con signo: negativa para ventas, positiva para
    devoluciones y ajustes (según el modelo de datos de la HU-08).

    Attributes:
        id: Identificador único del movimiento.
        producto_id: Identificador del producto afectado.
        tipo_movimiento: Tipo de operación que originó el movimiento.
        cantidad: Cantidad modificada, con signo.
        fecha_hora: Momento del cambio.
        documento_referencia_id: ID de la venta o devolución que originó el
            movimiento (opcional para ajustes manuales).
    """

    id: str
    producto_id: str
    tipo_movimiento: TipoMovimiento
    cantidad: int
    fecha_hora: datetime
    documento_referencia_id: str | None = None

    def __post_init__(self):
        if self.cantidad == 0:
            raise CantidadMovimientoInvalidaError(
                "La cantidad del movimiento no puede ser cero."
            )

        if self.tipo_movimiento is TipoMovimiento.VENTA and self.cantidad > 0:
            raise CantidadMovimientoInvalidaError(
                "Un movimiento de VENTA debe registrar una cantidad negativa."
            )

        if self.tipo_movimiento is TipoMovimiento.DEVOLUCION and self.cantidad < 0:
            raise CantidadMovimientoInvalidaError(
                "Un movimiento de DEVOLUCION debe registrar una cantidad positiva."
            )

    @classmethod
    def registrar(
        cls,
        *,
        id: str,
        producto_id: str,
        tipo_movimiento: TipoMovimiento,
        cantidad: int,
        fecha_hora: datetime,
        documento_referencia_id: str | None = None,
    ) -> "MovimientoStock":
        """Crea un movimiento a partir de la magnitud física de unidades movidas.

        Normaliza el signo de la cantidad según el tipo de movimiento, de modo
        que la lógica de signos viva en un único lugar del dominio.

        Args:
            id: Identificador único del movimiento.
            producto_id: Identificador del producto afectado.
            tipo_movimiento: Tipo de operación (VENTA, DEVOLUCION o AJUSTE).
            cantidad: Unidades físicas movidas; debe ser mayor a cero.
            fecha_hora: Momento del cambio.
            documento_referencia_id: ID del documento que originó el movimiento.

        Returns:
            El movimiento con la cantidad firmada según corresponda.

        Raises:
            CantidadMovimientoInvalidaError: Si la cantidad no es mayor a cero.
        """
        if cantidad <= 0:
            raise CantidadMovimientoInvalidaError(
                "La cantidad de unidades movidas debe ser mayor a cero."
            )

        if tipo_movimiento is TipoMovimiento.VENTA:
            cantidad = -cantidad

        return cls(
            id=id,
            producto_id=producto_id,
            tipo_movimiento=tipo_movimiento,
            cantidad=cantidad,
            fecha_hora=fecha_hora,
            documento_referencia_id=documento_referencia_id,
        )
