"""
Actualización de la Entidad de Dominio:
HU-01 implementacion de ventas y HU-05
implementacion de descuento
Para cumplir con la HU-04 y HU-07
(que mencionan el número de ticket) y facilitar
la validación de la HU-02, añadimos numero_ticket
a la entidad Venta y un método de dominio que evalúe
la elegibilidad para el cambio.

"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional

from app.domain.exceptions import PlazoDeCambioVencidoError
from app.domain.models.descuento import Descuento
from app.domain.models.detalle_venta import DetalleVenta

# Constante de regla de negocio transversal
MAX_DIAS_PARA_CAMBIO = 15


@dataclass
class Venta:
    id: str
    fecha_hora: datetime
    vendedor_id: str
    numero_ticket: str  # Nuevo campo para HU-04 y HU-07
    estado: str = "PENDIENTE"  # 'PENDIENTE', 'CONFIRMADA', 'CANCELADA'
    items: List[DetalleVenta] = field(default_factory=list)
    descuento: Descuento = field(default_factory=Descuento)

    def __post_init__(self):
        if self.estado not in ("PENDIENTE", "CONFIRMADA", "CANCELADA"):
            raise ValueError("Estado de venta inválido.")
        if not self.items:
            raise ValueError("Una venta debe tener al menos un item.")
        if self.fecha_hora is None:
            raise ValueError("La fecha y hora de la venta son obligatorias.")
        if not self.numero_ticket or not isinstance(self.numero_ticket, str):
            raise ValueError(
                "El número de ticket es obligatorio y debe ser una cadena de texto."
            )

    def confirmar(self) -> None:
        if self.estado != "PENDIENTE":
            raise ValueError("Solo se pueden confirmar ventas en estado PENDIENTE.")
        self.estado = "CONFIRMADA"

    def cancelar(self) -> None:
        if self.estado not in ("PENDIENTE", "CONFIRMADA"):
            raise ValueError("Solo se pueden cancelar ventas PENDIENTES o CONFIRMADAS.")
        self.estado = "CANCELADA"

    # --- Lógica de Dominio para HU-02 ---
    def validar_elegibilidad_para_cambio(self, fecha_solicitud: datetime) -> None:
        """
        Valida la regla de negocio transversal:
        Los cambios solo se permiten dentro de los 15 días calendario posteriores a la compra.
        Lanza PlazoDeCambioVencidoError si no cumple.
        """
        if self.estado != "CONFIRMADA":
            raise ValueError("Solo se pueden solicitar cambios de ventas CONFIRMADAS.")

        dias_transcurridos = (fecha_solicitud - self.fecha_hora).days

        if dias_transcurridos > MAX_DIAS_PARA_CAMBIO:
            raise PlazoDeCambioVencidoError(
                numero_ticket=self.numero_ticket,
                fecha_compra=self.fecha_hora.strftime("%Y-%m-%d"),
                dias_transcurridos=dias_transcurridos,
            )
