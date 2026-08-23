from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ItemVentaRequest(BaseModel):
    producto_id: str = Field(..., description="ID único del producto")
    cantidad: int = Field(
        ..., gt=0, description="Cantidad a vender, debe ser mayor a 0"
    )


class CrearVentaRequest(BaseModel):
    vendedor_id: str = Field(
        ..., description="ID del vendedor que realiza la operación"
    )
    items: list[ItemVentaRequest] = Field(
        ..., min_length=1, description="Lista de productos a vender"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "vendedor_id": "V-001",
                "items": [{"producto_id": "123", "cantidad": 2}],
            }
        }
    )


class ItemVentaResponse(BaseModel):
    producto_id: str
    nombre: str
    cantidad: int
    precio: float


class VentaResponse(BaseModel):
    id: str
    fecha_hora: datetime
    vendedor_id: str
    estado: str
    numero_ticket: str | None = None
    total: float | None = None
    mensaje: str | None = None
    items: list[ItemVentaResponse]

    model_config = ConfigDict(from_attributes=True)


class StockResponse(BaseModel):
    producto_id: str
    categoria: str
    nombre: str
    precio: int
    stock_actual: int


class ErrorResponse(BaseModel):
    error: str
    mensaje: str
    producto_id: str | None = None


class ItemTicketResponse(BaseModel):
    """Ítem de la compra original mostrado al validar un ticket (HU-04)."""

    producto_id: str
    nombre: str
    cantidad: int
    precio: float


class ValidarTicketResponse(BaseModel):
    """Respuesta exitosa al validar la existencia de un ticket (HU-04)."""

    existe: bool = Field(True, description="Indica que el ticket fue encontrado")
    numero_ticket: str
    fecha_compra: datetime
    cajero_original_id: str = Field(
        ..., description="ID del cajero/vendedor que registró la compra original"
    )
    items: list[ItemTicketResponse]
    mensaje: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "existe": True,
                "numero_ticket": "T-20260601-001",
                "fecha_compra": "2026-05-20T14:30:00Z",
                "cajero_original_id": "C-003",
                "items": [
                    {
                        "producto_id": "123",
                        "nombre": "Camiseta Azul",
                        "cantidad": 1,
                        "precio": 25.00,
                    }
                ],
                "mensaje": "Ticket válido. Puede continuar con el proceso de cambio.",
            }
        }
    )


class TicketNoEncontradoErrorResponse(BaseModel):
    """Respuesta cuando el ticket ingresado no existe en el sistema (HU-04)."""

    existe: bool = Field(False, description="Indica que el ticket no fue encontrado")
    error: str
    mensaje: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "existe": False,
                "error": "TICKET_NO_ENCONTRADO",
                "mensaje": (
                    "El número de ticket ingresado no existe en el sistema. "
                    "Verifique el comprobante."
                ),
            }
        }
    )


class MarcarEnCambioResponse(BaseModel):
    """Respuesta al retener un ticket en proceso de cambio (HU-04)."""

    numero_ticket: str
    estado: str
    mensaje: str
