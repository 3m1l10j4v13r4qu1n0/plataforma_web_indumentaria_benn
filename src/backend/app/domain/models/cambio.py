from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from app.domain.exceptions import DomainException


class EstadoCambio(str, Enum):
    """Estados posibles de un cambio de producto."""

    APROBADO = "APROBADO"
    RECHAZADO_PLAZO = "RECHAZADO_PLAZO"


@dataclass
class Cambio:
    """Entidad que representa un cambio de producto asociado a una venta."""

    id: str
    venta_original_id: str
    fecha_cambio: datetime
    cajero_id: str
    producto_a_cambiar_id: str
    nuevo_producto_id: str
    estado: EstadoCambio
    motivo: str | None = None
    fecha_compra_original: datetime | None = None

    def __post_init__(self):
        if not self.venta_original_id:
            raise DomainException("El ID de la venta original es obligatorio.")

        if not self.cajero_id:
            raise DomainException("El ID del cajero es obligatorio.")

        if not self.producto_a_cambiar_id:
            raise DomainException("El ID del producto a cambiar es obligatorio.")

        if not self.nuevo_producto_id:
            raise DomainException("El ID del nuevo producto es obligatorio.")

        if self.producto_a_cambiar_id == self.nuevo_producto_id:
            raise DomainException(
                "El producto a cambiar y el nuevo producto no pueden ser el mismo."
            )

    def esta_dentro_del_plazo(self, dias_limite: int = 15) -> bool:
        """Verifica si el cambio está dentro del plazo permitido.

        Args:
            dias_limite: Número máximo de días permitidos para cambios.

        Returns:
            True si está dentro del plazo, False en caso contrario.
        """
        if self.fecha_compra_original is None:
            return False

        fecha_actual = datetime.now()
        diferencia = fecha_actual - self.fecha_compra_original
        return diferencia.days <= dias_limite

    def calcular_dias_transcurridos(self) -> int:
        """Calcula los días transcurridos desde la compra original.

        Returns:
            Número de días transcurridos.
        """
        if self.fecha_compra_original is None:
            return 0

        fecha_actual = datetime.now()
        diferencia = fecha_actual - self.fecha_compra_original
        return diferencia.days
