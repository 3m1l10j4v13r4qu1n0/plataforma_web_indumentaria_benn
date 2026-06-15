from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Optional

from app.domain.exceptions import (
    CantidadMovimientoInvalidaError,
    TipoMovimientoInvalidoError,
)

TipoMovimiento = Literal["VENTA", "DEVOLUCION", "CAMBIO", "AJUSTE"]


@dataclass(frozen=True)
class MovimientoStock:
    id: str
    producto_id: str
    cantidad: int  # Negativo para egresos (venta), positivo para ingresos (devolución)
    tipo_movimiento: TipoMovimiento
    referencia_id: Optional[str]  # ID de la Venta, Cambio o nota de ajuste
    fecha_hora: datetime

    def __post_init__(self):
        # Validación de invariante: El tipo de movimiento debe ser válido
        if self.tipo_movimiento not in ("VENTA", "DEVOLUCION", "CAMBIO", "AJUSTE"):
            raise TipoMovimientoInvalidoError(self.tipo_movimiento)

        # Validación de invariante: La cantidad no puede ser cero
        if self.cantidad == 0:
            raise CantidadMovimientoInvalidaError(self.cantidad)
