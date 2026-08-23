from dataclasses import dataclass


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
