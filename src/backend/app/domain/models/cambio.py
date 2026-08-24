from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from app.domain.exceptions import (
    DomainException,
    ObservacionesRequeridasError,
)


class EstadoCambio(str, Enum):
    """Estados posibles de un cambio de producto."""

    APROBADO = "APROBADO"
    RECHAZADO_PLAZO = "RECHAZADO_PLAZO"
    RECHAZADO_ESTADO_PRODUCTO = "RECHAZADO_ESTADO_PRODUCTO"


class EstadoProducto(str, Enum):
    """Estado físico del producto presentado para cambio (HU-03)."""

    NUEVO_ETIQUETADO = "NUEVO_ETIQUETADO"
    USADO = "USADO"
    DANADO = "DANADO"


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
    estado_producto: EstadoProducto | None = None
    tiene_etiqueta: bool | None = None
    observaciones: str | None = None
    fecha_validacion: datetime | None = None

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

    def es_apto_para_cambio(self) -> bool:
        """Verifica si el producto físico es apto para el cambio (HU-03).

        Un producto es apto únicamente si su estado es NUEVO_ETIQUETADO
        y conserva la etiqueta original.

        Returns:
            True si el producto es apto, False en caso contrario.
        """
        return (
            self.estado_producto == EstadoProducto.NUEVO_ETIQUETADO
            and self.tiene_etiqueta is True
        )

    def validar_estado_fisico(self) -> str | None:
        """Valida el estado físico del producto para aceptar el cambio (HU-03).

        Si el producto no es apto, exige registrar observaciones del rechazo
        (auditoría) y devuelve el motivo correspondiente.

        Returns:
            None si el producto es apto; en caso contrario, el código del
            motivo de rechazo.

        Raises:
            ObservacionesRequeridasError: si el producto no es apto y no se
                registraron observaciones del rechazo.
        """
        motivo = self.obtener_motivo_rechazo()

        if motivo is not None and not self.observaciones:
            raise ObservacionesRequeridasError()

        return motivo

    def obtener_motivo_rechazo(self) -> str | None:
        """Determina el motivo de rechazo del producto (HU-03).

        Returns:
            None si el producto es apto para el cambio; en caso contrario,
            el código del motivo de rechazo.
        """
        if self.es_apto_para_cambio():
            return None

        if self.estado_producto == EstadoProducto.USADO:
            return "PRODUCTO_USADO"

        if self.estado_producto == EstadoProducto.DANADO:
            return "PRODUCTO_DANADO"

        return "PRODUCTO_SIN_ETIQUETA"
