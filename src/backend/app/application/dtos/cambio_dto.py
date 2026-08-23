from dataclasses import dataclass

from app.domain.models.cambio import EstadoProducto


@dataclass
class ConsultarVentaPorTicketQuery:
    numero_ticket: str


@dataclass
class ProcesarCambioCommand:
    venta_original_id: str
    cajero_id: str
    producto_a_cambiar_id: str
    nuevo_producto_id: str
    motivo: str | None = None


@dataclass
class ValidarEstadoProductoCommand:
    """Datos de la inspección física del producto (HU-03)."""

    cambio_id: str
    producto_id: str
    estado_producto: EstadoProducto
    tiene_etiqueta: bool
    observaciones: str | None = None
    cajero_id: str | None = None


@dataclass
class ValidarEstadoProductoResult:
    """Resultado de la validación de estado físico del producto (HU-03)."""

    es_apto_para_cambio: bool
    mensaje: str
